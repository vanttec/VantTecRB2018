package mx.tec.vanttec.dron

import android.content.Context
import android.preference.PreferenceManager
import java.net.Inet4Address
import java.net.Socket

class BaseConnection(context: Context) {
    private val socket: Socket

    init {
        val prefs = PreferenceManager.getDefaultSharedPreferences(context)

        val baseAddr = prefs.getString("base_addr", "192.168.0.201")
        val port = prefs.getString("base_port", "5000")

        socket = Socket(baseAddr, port.toInt())
    }
}