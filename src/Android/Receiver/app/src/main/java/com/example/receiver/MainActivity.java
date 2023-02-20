package com.example.receiver;

import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager2.widget.ViewPager2;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanRecord;
import android.bluetooth.le.ScanResult;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;

import com.google.android.material.tabs.TabLayout;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.util.Calendar;
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

    TabLayout tabLayout;
    ViewPager2 viewPager2;
    MyViewPagerAdapter myViewPagerAdapter;

    @SuppressLint("MissingPermission")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (!mBluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, 1);
        }

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

    public static String getURL() {
        return urlServer;
    }

    public static void setURL(String url) {
        urlServer = url;
    }

    private static ScanCallback scanCallback = new ScanCallback() {
        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            BluetoothDevice device = result.getDevice();
            String bleDevice = device.getAddress();

            String b1 = "CA:F4:06:34:9C:31";
            String b2 = "D9:27:C2:C1:22:38";
            String b3 = "CC:B9:16:CD:6F:2F";
            String b4 = "F6:C1:78:1C:4F:2D";
            String b5 = "EB:76:88:9B:81:63";
            String b6 = "FD:D0:C6:19:B1:E9";

            if (
                Objects.equals(bleDevice, b1) ||
                Objects.equals(bleDevice, b2) ||
                Objects.equals(bleDevice, b3) ||
                Objects.equals(bleDevice, b4) ||
                Objects.equals(bleDevice, b5) ||
                Objects.equals(bleDevice, b6))
            {
                // Send data to server
                RequestBody formbody
                        = new FormBody.Builder()
                        .add("Timestamp", String.valueOf(Calendar.getInstance().getTimeInMillis()))
                        .add("ReceiverDevice", Build.MODEL + " (" + Build.ID + ")")
                        .add("BLEDevice", bleDevice)
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
        }
    };

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