package mx.tec.vanttec.dron

import android.content.Context
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView

class SettingsAdapter(context: Context) :
        RecyclerView.Adapter<SettingsAdapter.SettingViewHolder>() {

    private val prefs = context.getSharedPreferences("vanttec_drone", Context.MODE_PRIVATE)

    private val keys = arrayOf(
            "Base address" to Setting("base", Setting.Type.STRING),
            "Default altitude" to Setting("alt", Setting.Type.FLOAT)
    )

    override fun getItemCount(): Int {
        return keys.size
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): SettingViewHolder {
        val view = LayoutInflater.from(parent.context)
                .inflate(R.layout.item_setting, parent, false)

        return SettingViewHolder(view)
    }

    override fun onBindViewHolder(holder: SettingViewHolder, position: Int) {
        val (title, setting) = keys[position]

        val data = when(setting.type) {
            Setting.Type.BOOL    -> prefs.getBoolean(setting.key, false).toString()
            Setting.Type.STRING  -> prefs.getString(setting.key, "None")
            Setting.Type.INT     -> prefs.getInt(setting.key, 0).toString()
            Setting.Type.FLOAT   -> prefs.getFloat(setting.key, 0f).toString()
        }

        holder.title.text = title
        holder.value.text = data

        holder.itemView.setOnClickListener {

        }
    }

    class SettingViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val title = view.findViewById<TextView>(R.id.title)!!
        val value = view.findViewById<TextView>(R.id.value)!!
    }
}