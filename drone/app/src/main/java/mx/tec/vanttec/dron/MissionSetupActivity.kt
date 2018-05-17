package mx.tec.vanttec.dron

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.graphics.SurfaceTexture
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Build
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.view.TextureView
import android.widget.Toast
import android.view.WindowManager

import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.*

import dji.common.camera.SettingsDefinitions
import dji.common.error.DJIError
import dji.common.mission.waypoint.*
import dji.common.product.Model
import dji.sdk.base.BaseProduct
import dji.sdk.camera.VideoFeeder
import dji.sdk.codec.DJICodecManager
import dji.sdk.mission.MissionControl
import dji.sdk.mission.waypoint.WaypointMissionOperatorListener
import dji.sdk.products.Aircraft
import dji.sdk.sdkmanager.DJISDKManager
import io.reactivex.Single
import io.reactivex.functions.BiFunction

import kotlinx.android.synthetic.main.activity_mission_setup.*

class MissionSetupActivity : AppCompatActivity(),
        TextureView.SurfaceTextureListener {

    private val missionMap = MissionMap(supportFragmentManager)
    private val sdk = DJISDKManager.getInstance()
    private var mCodecManager: DJICodecManager? = null // Codec for video live view
    private val djiApplication = application as DJIApplication

    private val mReceivedVideoDataCallBack = VideoFeeder.VideoDataCallback { videoBuffer, size ->
        mCodecManager?.sendDataToDecoder(videoBuffer, size)
    }

    private var missionControl: MissionControl? = null
        get() {
            if(sdk.hasSDKRegistered()) {
                return sdk.missionControl
            }

            return null
        }

    private var product: BaseProduct? = null

    private var waypointMissionBuilder = WaypointMission.Builder()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // When the compile and target version is higher than 22, please request the
        // following permissions at runtime to ensure the
        // SDK work well.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            requestPermissions(
                    arrayOf(
                            Manifest.permission.WRITE_EXTERNAL_STORAGE,
                            Manifest.permission.VIBRATE,
                            Manifest.permission.INTERNET,
                            Manifest.permission.ACCESS_WIFI_STATE,
                            Manifest.permission.WAKE_LOCK,
                            Manifest.permission.ACCESS_NETWORK_STATE,
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.CHANGE_WIFI_STATE,
                            Manifest.permission.MOUNT_UNMOUNT_FILESYSTEMS,
                            Manifest.permission.READ_EXTERNAL_STORAGE,
                            Manifest.permission.SYSTEM_ALERT_WINDOW,
                            Manifest.permission.READ_PHONE_STATE
                    ),
                    1
            )
        }

        setContentView(R.layout.activity_mission_setup)

        initUI()

        // Map async
        val mapFragment = supportFragmentManager.findFragmentById(R.id.mapFragment) as SupportMapFragment
        mapFragment.getMapAsync(missionMap)

        // Hide keyboard
        window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_HIDDEN)
        // Prevent screen from locking
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        missionMap.waypointObservable.subscribe {
            waypointMissionBuilder.addWaypoint(it)
        }

        val productObservable = djiApplication.sdkManagerCallback?.productObservable
        productObservable?.subscribe {
            product = it
            if(it is Aircraft){
                it.flightController.setStateCallback { state ->
                    runOnUiThread {
                        val pos = LatLng(state.aircraftLocation.latitude, state.aircraftLocation.longitude)
                        val head = it.flightController.compass.heading
                        missionMap.updateMarker(pos, head)
                    }
                }
            }
        }
    }

    override fun onResume() {
        super.onResume()
        initPreviewer()
    }

    override fun onPause() {
        destroyPreviewer()
        super.onPause()
    }

    override fun onDestroy() {
        // Remove waypoint missions listener
        destroyPreviewer()
        super.onDestroy()
    }

    /*********************
     * Activity init functions
     */

    // Init view layout variables
    private fun initUI() {
        liveFeed.surfaceTextureListener = this
        locate.setOnClickListener { centerCameraOnLocation() }
        takeOff.setOnClickListener { configWayPointMission() }
        addPin.setOnClickListener { toggleAddPin() }
    }

    private fun toggleAddPin() {
        missionMap.toggleAddPin()

        val color = if(missionMap.shouldAddPin)
            resources.getColor(R.color.colorPrimary, theme)
        else
            resources.getColor(R.color.white, theme)

        addPin.setColorFilter(color)
    }

    private fun centerCameraOnLocation() {
        val permission = checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION)

        if(permission == PackageManager.PERMISSION_GRANTED) {
            val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager

            val lastLocation = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)

            val listener = object : LocationListener {
                override fun onLocationChanged(location: Location?) {
                    Log.d(TAG, "Location changed!")
                    if(location != null) {
                        val lat = location.latitude
                        val lng = location.longitude
                        val cameraUpdate = CameraUpdateFactory.newLatLngZoom(LatLng(lat, lng), 18f)

                        missionMap.moveCamera(cameraUpdate)
                        locationManager.removeUpdates(this)
                    }
                }

                override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {}

                override fun onProviderEnabled(provider: String?) {}

                override fun onProviderDisabled(provider: String?) {}
            }

            locationManager.requestLocationUpdates(
                    LocationManager.GPS_PROVIDER,
                    1000,
                    1f,
                    listener)

            val cameraUpdate = CameraUpdateFactory.newLatLngZoom(
                    LatLng(lastLocation.latitude, lastLocation.longitude),
                    17f)

            missionMap.moveCamera(cameraUpdate)
        }
    }

    private fun initPreviewer() {
        if (product?.isConnected == true) {
            setResultToToast(getString(R.string.disconnected))
        } else {
            liveFeed.surfaceTextureListener = this
            if (product?.model != Model.UNKNOWN_AIRCRAFT) {
                VideoFeeder.getInstance()?.primaryVideoFeed?.callback = mReceivedVideoDataCallBack
            }
        }
    }

    private fun destroyPreviewer() {
        if (product?.camera != null) {
            VideoFeeder.getInstance().primaryVideoFeed.callback = null
        }
    }

    private fun switchCameraMode(cameraMode: SettingsDefinitions.CameraMode) {
        product?.camera?.setMode(cameraMode) { error ->
            if (error == null) {
                setResultToToast("Switch Camera Mode Succeeded")
            } else {
                setResultToToast(error.description)
            }
        }
    }

    private fun configWayPointMission() {

        val mSpeed = 3.0f
        waypointMissionBuilder.finishedAction(WaypointMissionFinishedAction.GO_HOME)
                .headingMode(WaypointMissionHeadingMode.AUTO)
                .autoFlightSpeed(mSpeed)
                .maxFlightSpeed(mSpeed)
                .flightPathMode(WaypointMissionFlightPathMode.NORMAL)

        val waypointMissionOperator = missionControl?.waypointMissionOperator

        if(waypointMissionOperator != null) {
            val error = waypointMissionOperator.loadMission(waypointMissionBuilder.build())
            if (error == null) {
                setResultToToast("loadWaypoint succeeded")
                uploadWayPointMission()
            } else {
                setResultToToast("loadWaypoint failed " + error.description)
            }
        }
    }

    private fun uploadWayPointMission() {
        val waypointMissionOperator = missionControl?.waypointMissionOperator

        waypointMissionOperator?.uploadMission { error ->
            if (error == null) {
                waypointMissionOperator.addListener(object : WaypointMissionOperatorListener {
                    override fun onExecutionFinish(p0: DJIError?) {
                        //Blank
                    }

                    override fun onExecutionStart() {
                        //Blank
                    }

                    override fun onUploadUpdate(event: WaypointMissionUploadEvent?) {
                        if(event?.currentState == WaypointMissionState.READY_TO_EXECUTE)
                            startWaypointMission()
                    }

                    override fun onDownloadUpdate(p0: WaypointMissionDownloadEvent?) {
                        //Blank
                    }

                    override fun onExecutionUpdate(p0: WaypointMissionExecutionEvent?) {
                        //Blank
                    }

                })
            } else {
                setResultToToast("Mission upload failed, error: " + error.description + " retrying...")
            }
        }
    }

    private fun startWaypointMission() {
        val waypointMissionOperator = missionControl?.waypointMissionOperator

        switchCameraMode(SettingsDefinitions.CameraMode.SHOOT_PHOTO)

        waypointMissionOperator?.startMission { error ->
            val status = if (error == null) "Success" else error.description
            setResultToToast("Mission Start: $status")
        }
    }

    /***********************
     * Live feed functions
     */

    override fun onSurfaceTextureAvailable(surface: SurfaceTexture, width: Int, height: Int) {
        val surfaceSingle = Single.just(surface)
        val registerSubject = djiApplication.sdkManagerCallback?.registerSubject

        val both = surfaceSingle.zipWith<DJIError, DJICodecManager>(registerSubject, BiFunction { surface, _ ->
             DJICodecManager(this, surface, width, height)
        })

       both.subscribe { it ->
           mCodecManager = it
       }

    }

    override fun onSurfaceTextureSizeChanged(surface: SurfaceTexture, width: Int, height: Int) {
        Log.e(TAG, "onSurfaceTextureSizeChanged")
    }

    override fun onSurfaceTextureDestroyed(surface: SurfaceTexture): Boolean {
        Log.e(TAG, "onSurfaceTextureDestroyed")
        mCodecManager?.cleanSurface()
        mCodecManager = null

        return false
    }

    override fun onSurfaceTextureUpdated(surface: SurfaceTexture) {}

    /********************
     * Helper functions
     */

    private fun setResultToToast(string: String) {
        runOnUiThread { Toast.makeText(this, string, Toast.LENGTH_SHORT).show() }
    }

    companion object {
        private const val TAG = "Main Activity"
    }
}
