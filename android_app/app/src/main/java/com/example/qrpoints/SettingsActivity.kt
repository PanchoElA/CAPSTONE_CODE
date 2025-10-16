package com.example.qrpoints

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity

class SettingsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        val serverInput = findViewById<EditText>(R.id.inputServer)
        val prefs = getSharedPreferences("qrpoints", MODE_PRIVATE)
        val current = prefs.getString("server_base", "http://192.168.5.53:5000") ?: "http://192.168.5.53:5000"
        serverInput.setText(current)

        findViewById<Button>(R.id.btnSave).setOnClickListener {
            val v = serverInput.text.toString().trim()
            if (v.isNotEmpty()) {
                prefs.edit().putString("server_base", v).apply()
                finish()
            }
        }

        findViewById<Button>(R.id.btnCancel).setOnClickListener {
            finish()
        }
    }
}
