package mx.tec.vanttec.dron

import android.app.Application
import android.content.Context
import android.support.multidex.MultiDex
import com.secneo.sdk.Helper

import dji.sdk.sdkmanager.DJISDKManager

class DJIApplication : Application() {
    var sdkManagerCallback : SDKManagerCallback? = null

    override fun attachBaseContext(base: Context) {
        super.attachBaseContext(base)
        MultiDex.install(this)
        Helper.install(this)

        val instance = DJISDKManager.getInstance()
        sdkManagerCallback = SDKManagerCallback()

        instance.registerApp(base, sdkManagerCallback)

        System.loadLibrary("opencv_java3")
    }
}
