package mx.tec.vanttec.dron

import android.app.AlertDialog
import android.app.Dialog
import android.support.v4.app.DialogFragment
import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.widget.EditText
import com.google.android.gms.maps.model.LatLng

class WayPointDialog : DialogFragment() {
    var listener: WayPointConfigListener? = null

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val builder = AlertDialog.Builder(activity)

        val inflater = context?.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
        val view = inflater.inflate(R.layout.dialog_waypoint, null)

        val latitude = view.findViewById<EditText>(R.id.latitude)
        val longitud = view.findViewById<EditText>(R.id.longitud)
        val height = view.findViewById<EditText>(R.id.height)
        val time = view.findViewById<EditText>(R.id.time)

        latitude.setText(arguments?.getDouble(LAT_ARG).toString())
        longitud.setText(arguments?.getDouble(LNG_ARG).toString())
        height.setText(arguments?.getFloat(HEIGHT_ARG).toString())
        time.setText("0")

        builder.setView(view)

        builder.setPositiveButton(android.R.string.ok) { dialog , _ ->
            val lat = latitude.text.toString().toDouble()
            val lng = longitud.text.toString().toDouble()
            val height = height.text.toString().toFloat()
            val time = time.text.toString().toFloat() * 1000 // Time in ms

            listener?.onWayPointConfigured(LatLng(lat, lng), height, time.toInt())
            dialog.dismiss()
        }

        builder.setNegativeButton(android.R.string.cancel) { dialog, _ ->
            listener?.onWayPointCancelled()
            dialog.dismiss()
        }

        return builder.create()
    }

    override fun onAttach(context: Context?) {
        super.onAttach(context)
    }

    companion object {
        private const val LAT_ARG = "lat_argument"
        private const val LNG_ARG = "lng_argument"
        private const val HEIGHT_ARG = "height_argument"

        fun instantiate(point: LatLng, height: Float) : WayPointDialog {
            val dlg = WayPointDialog()
            val bnd = Bundle()

            bnd.putDouble(LAT_ARG, point.latitude)
            bnd.putDouble(LNG_ARG, point.longitude)
            bnd.putFloat(HEIGHT_ARG, height)

            dlg.arguments = bnd

            return dlg
        }
    }

    interface WayPointConfigListener {
        fun onWayPointConfigured(point: LatLng, height: Float, time: Int)
        fun onWayPointCancelled()
    }
}