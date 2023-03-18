package com.example.receiver;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.viewpager2.widget.ViewPager2;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;

import com.google.android.material.tabs.TabLayout;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.Objects;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    private static String urlServer = "http://192.168.0.100:5000";
    private static OkHttpClient okHttpClient;
    private static Request request;
    private static BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    private static BluetoothLeScanner scanner;

    private static final int PERMISSIONS_REQUEST_CODE = 1;

    TabLayout tabLayout;
    ViewPager2 viewPager2;
    MyViewPagerAdapter myViewPagerAdapter;

    @Override
    @SuppressLint("MissingPermission")
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Checks if all required permissions have been granted
        checkPermissions();

        // Asks to enable phone bluetooth
        checkBluetoothTurnedOn();

        setContentView(R.layout.activity_main);
        tabLayout = findViewById(R.id.tab_layout);
        viewPager2 = findViewById(R.id.view_pager);
        myViewPagerAdapter = new MyViewPagerAdapter(this);
        viewPager2.setAdapter(myViewPagerAdapter);
        viewPager2.setUserInputEnabled(false);

        tabLayout.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                viewPager2.setCurrentItem(tab.getPosition());
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {

            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {

            }
        });

        viewPager2.registerOnPageChangeCallback(new ViewPager2.OnPageChangeCallback() {
            @Override
            public void onPageSelected(int position) {
                super.onPageSelected(position);
                tabLayout.getTabAt(position).select();
            }
        });
    }

    private void checkPermissions() {
        String[] permissions = {
                android.Manifest.permission.BLUETOOTH_CONNECT,
                android.Manifest.permission.BLUETOOTH_SCAN,
                android.Manifest.permission.ACCESS_FINE_LOCATION,
        };

        List<String> permissionsToRequest = new ArrayList<>();
        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(permission);
            }
        }

        if (!permissionsToRequest.isEmpty()) {
            ActivityCompat.requestPermissions(this, permissionsToRequest.toArray(new String[0]), PERMISSIONS_REQUEST_CODE);
        }
    }

    private void checkBluetoothTurnedOn() {
        if (!mBluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            ActivityResultLauncher<Intent> launcher = registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == Activity.RESULT_OK) {
                    // Bluetooth is now enabled, handle the success case
                } else {
                    // User did not enable Bluetooth, handle the failure case
                }
            });
            launcher.launch(enableBtIntent);
        }
    }

    @Override
    @SuppressLint("MissingSuperCall")
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSIONS_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // permission was granted
            } else if (grantResults.length > 0 && grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                // permission denied
                new AlertDialog.Builder(this)
                    .setMessage("L'application doit utiliser les fonctionnalités bluetooth.\n\n" +
                                "Vous devez accorder l'autorisation d'accéder aux 'Appareils à proximité'.")
                    .setPositiveButton("Paramètres", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int which) {
                            // Request the permission again
                            Intent intent = new Intent();
                            intent.setAction(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
                            Uri uri = Uri.fromParts("package", getPackageName(), null);
                            intent.setData(uri);
                            startActivity(intent);
                        }
                    })
                    .setNegativeButton("Quitter", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int which) {
                            // User cancelled the dialog, take some action
                            finishAffinity();
                        }
                    })
                    .show();
            }
        }
    }

    private static ScanCallback scanCallback = new ScanCallback() {
        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            BluetoothDevice device = result.getDevice();

            // Send data to server
            RequestBody formbody
                    = new FormBody.Builder()
                    .add("Timestamp", String.valueOf(Calendar.getInstance().getTimeInMillis()))
                    .add("ReceiverDevice", Build.MODEL + " (" + Build.ID + ")")
                    .add("BLEDevice", device.getAddress())
                    .add("RSSI", String.valueOf(result.getRssi()))
                    .build();
            Request request = new Request.Builder().url(getURL() + "/ble")
                    .post(formbody)
                    .build();

            okHttpClient.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(
                        @NotNull Call call,
                        @NotNull IOException e) {
                        /*
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(getApplicationContext(), "server down", Toast.LENGTH_SHORT).show();
                            }
                        });
                        */
                }

                @Override
                public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                    /*
                    if (response.body().string().equals("received")) {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(getApplicationContext(), "data received", Toast.LENGTH_SHORT).show();
                            }
                        });
                    }
                    */
                }
            });
        }
    };

    public static String getURL() {
        return urlServer;
    }

    public static void setURL(String url) {
        urlServer = url;
    }

    @SuppressLint("MissingPermission")
    public static void startScan() {
        okHttpClient = new OkHttpClient();
        request = new Request.Builder().url(getURL()).build();
        scanner = mBluetoothAdapter.getBluetoothLeScanner();

        if (scanner != null) {
            scanner.startScan(scanCallback);
        }
    }

    @SuppressLint("MissingPermission")
    public static void stopScan() {
        scanner.stopScan(scanCallback);
    }
}