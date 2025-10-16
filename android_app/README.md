# QRPoints Android App

This is a minimal Android app that scans QR codes and awards points for codes prefixed with `MYAPPPOINTS:`.

Requirements:
- Android Studio (recommended) or Gradle + SDK
- A physical Android device (recommended for camera testing)

How to run:
1. Open the `android_app` folder in Android Studio.
2. Let Gradle sync and install required dependencies.
3. Connect your Android device (enable Developer Options + USB debugging) or use an emulator with camera support.
4. Run the app from Android Studio.

Notes:
- The app uses CameraX and ML Kit Barcode Scanning.
	- If you get `Failed to resolve: com.google.mlkit:barcode-scanning`, ensure you have `google()` and `mavenCentral()` in your repositories and try Gradle sync again. The project includes these repositories but network or cached issues can still cause failures.
- Points and scan history are stored in `SharedPreferences`.
- Valid QR format: `MYAPPPOINTS:<id>` (e.g., `MYAPPPOINTS:abc123`).

If you want improvements (Room persistence, better UI, Compose), tell me and I can add them.
