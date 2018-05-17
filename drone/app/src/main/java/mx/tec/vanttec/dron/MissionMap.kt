package mx.tec.vanttec.dron

import android.support.v4.app.FragmentManager
import com.google.android.gms.maps.CameraUpdate
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.model.*
import dji.common.mission.waypoint.Waypoint
import dji.common.mission.waypoint.WaypointAction
import dji.common.mission.waypoint.WaypointActionType
import io.reactivex.Observable

class MissionMap(private val fragmentManager: FragmentManager) : GoogleMap.OnMapClickListener,
        OnMapReadyCallback {

    private val mMarkers = ArrayList<Marker>()
    private val defaultAltitude = 12f
    private var gMap: GoogleMap? = null
    private var droneMarker: Marker? = null
    private lateinit var waypointListener: WayPointDialog.WayPointConfigListener

    var shouldAddPin = false
        private set

    val waypointObservable = Observable.create<Waypoint> {
        waypointListener =  object : WayPointDialog.WayPointConfigListener {
            override fun onWayPointConfigured(point: LatLng, height: Float, time: Int) {
                markWaypoint(point)
                val waypoint = Waypoint(point.latitude, point.longitude, height)
                waypoint.addAction(WaypointAction(WaypointActionType.STAY, time))

                it.onNext(waypoint)
            }

            override fun onWayPointCancelled() {
                // Do nothing
            }
        }
    }.publish()

    init {
        waypointObservable.connect()
    }

    private fun markWaypoint(point: LatLng) {
        //Create MarkerOptions object
        val markerOptions = MarkerOptions()
        markerOptions.position(point)
        markerOptions.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_BLUE))
        val marker = gMap?.addMarker(markerOptions)

        if(marker != null)
            mMarkers.add(marker)
    }

    override fun onMapReady(googleMap: GoogleMap) {
        if (gMap == null) {
            gMap = googleMap
            gMap?.setOnMapClickListener(this)// add the listener for click for a map object
        }

        val tec = LatLng(25.65, -100.290943)
        gMap?.moveCamera(CameraUpdateFactory.newLatLng(tec))
        gMap?.mapType = GoogleMap.MAP_TYPE_NORMAL
    }

    override fun onMapClick(point: LatLng) {
        if (shouldAddPin) {
            // Open waypoint dialog
            val waypointDialog = WayPointDialog.instantiate(point, defaultAltitude)

            waypointDialog.listener = waypointListener
            waypointDialog.show(fragmentManager, "waypoint_dialog")
        }
    }

    // Drone state
    fun updateMarker(position: LatLng, heading: Float) {
        if(droneMarker == null) {
            val options = MarkerOptions()
            val icon = BitmapDescriptorFactory.fromResource(R.drawable.aircraft)

            options.position(position)
                .rotation(heading)
                .icon(icon)
                .anchor(0.5f,0.5f)

            droneMarker = gMap?.addMarker(options)
        } else {
            droneMarker?.position = position
            droneMarker?.rotation = heading
        }
    }

    fun toggleAddPin() {
        shouldAddPin = !shouldAddPin
    }

    fun moveCamera(cameraUpdate: CameraUpdate) {
        gMap?.moveCamera(cameraUpdate)
    }
}