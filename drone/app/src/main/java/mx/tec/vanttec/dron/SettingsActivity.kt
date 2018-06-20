package mx.tec.vanttec.dron

import android.os.Bundle
import android.os.PersistableBundle
import android.support.v7.app.AppCompatActivity
import android.support.v7.widget.LinearLayoutManager

import kotlinx.android.synthetic.main.activity_settings.*

class SettingsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?, persistentState: PersistableBundle?) {
        super.onCreate(savedInstanceState, persistentState)

        setContentView(R.layout.activity_settings)

        recyclerView.apply {
            adapter = SettingsAdapter(this@SettingsActivity)
            layoutManager = LinearLayoutManager(this@SettingsActivity)
            setHasFixedSize(true)
        }
    }

}