package com.example.qrpoints

import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity

class HomeActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        findViewById<View>(R.id.btnScan).setOnClickListener {
            promptForProfile { profile ->
                val i = Intent(this, ScanActivity::class.java)
                i.putExtra("profile", profile)
                startActivity(i)
            }
        }

        findViewById<View>(R.id.btnPoints).setOnClickListener {
            // Open PointsActivity without specifying a profile to show all profiles
            startActivity(Intent(this, PointsActivity::class.java))
        }

        findViewById<View>(R.id.btnSettings).setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }
    }

    private fun promptForProfile(onOk: (String) -> Unit) {
        val input = EditText(this)
        input.hint = "Nombre (ej. Juan)"
        input.imeOptions = android.view.inputmethod.EditorInfo.IME_ACTION_DONE
        input.isSingleLine = true
        input.inputType = android.text.InputType.TYPE_CLASS_TEXT
        val dialog = AlertDialog.Builder(this)
            .setTitle("¿A nombre de quién guardamos los puntos?")
            .setView(input)
            .setPositiveButton("Ok") { _, _ ->
                val profile = input.text.toString().trim().ifEmpty { "default" }
                onOk(profile)
            }
            .setNegativeButton("Cancelar", null)
            .create()

        // Allow pressing the keyboard's Done/Enter to submit
        input.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == android.view.inputmethod.EditorInfo.IME_ACTION_DONE) {
                val profile = input.text.toString().trim().ifEmpty { "default" }
                dialog.dismiss()
                onOk(profile)
                true
            } else false
        }

        // Fallback: handle physical Enter key
        input.setOnKeyListener { _, keyCode, event ->
            if (keyCode == android.view.KeyEvent.KEYCODE_ENTER && event.action == android.view.KeyEvent.ACTION_UP) {
                val profile = input.text.toString().trim().ifEmpty { "default" }
                dialog.dismiss()
                onOk(profile)
                true
            } else false
        }

        dialog.show()

        // Ensure keyboard is shown and input focused
        input.requestFocus()
        val imm = getSystemService(android.content.Context.INPUT_METHOD_SERVICE) as? android.view.inputmethod.InputMethodManager
        imm?.showSoftInput(input, android.view.inputmethod.InputMethodManager.SHOW_IMPLICIT)
    }
}
