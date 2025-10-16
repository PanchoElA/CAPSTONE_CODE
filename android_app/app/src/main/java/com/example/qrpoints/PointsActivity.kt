package com.example.qrpoints

import android.os.Bundle
import android.view.View
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class PointsActivity : AppCompatActivity() {
    private lateinit var pointsManager: PointsManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_points)

        pointsManager = PointsManager(this)

        val profile = intent.getStringExtra("profile") ?: "default"

        val pointsTitle = findViewById<TextView>(R.id.pointsTitle)
        // If activity started without an explicit profile, show all profiles list
        if (intent.hasExtra("profile")) {
            pointsTitle.text = "Puntos acumulados - $profile"
            val pointsValue = findViewById<TextView>(R.id.pointsValue)
            pointsValue.text = pointsManager.getPoints(profile).toString()
        } else {
            pointsTitle.text = "Puntos por perfil"
            findViewById<TextView>(R.id.pointsValue).visibility = View.GONE
            val container = findViewById<android.widget.LinearLayout>(R.id.profilesContainer)
            container.visibility = View.VISIBLE
            container.removeAllViews()
            val profiles = pointsManager.getProfiles()
            if (profiles.isEmpty()) {
                val tv = TextView(this)
                tv.text = "No hay perfiles todavía"
                container.addView(tv)
            } else {
                for (p in profiles) {
                    val row = TextView(this)
                    row.text = "$p: ${pointsManager.getPoints(p)} puntos"
                    row.textSize = 18f
                    row.setPadding(8, 8, 8, 8)
                    container.addView(row)
                }
            }
        }

        findViewById<View>(R.id.btnBack).setOnClickListener {
            finish()
        }
    }
}
