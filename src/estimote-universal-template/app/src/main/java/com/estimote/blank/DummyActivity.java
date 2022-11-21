package com.estimote.blank;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.estimote.internal_plugins_api.scanning.BluetoothScanner;
import com.estimote.internal_plugins_api.scanning.EstimoteTelemetryFrameA;
import com.estimote.internal_plugins_api.scanning.ScanHandler;
import com.estimote.proximity_sdk.api.EstimoteCloudCredentials;
import com.estimote.scanning_plugin.api.EstimoteBluetoothScannerFactory;

import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.io.IOException;

import kotlin.Unit;
import kotlin.jvm.functions.Function1;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class DummyActivity extends AppCompatActivity {

    private EditText X, Y, message;
    private Button button;
    private OkHttpClient okHttpClient;

    EstimoteCloudCredentials estimoteCloudCredentials =
            new EstimoteCloudCredentials("universal-template-4r8", "697ce7ec7ffb494e88d6c782a698b95e");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dummy);
        X = findViewById(R.id.dummy_text);
        Y = findViewById(R.id.dummy_text2);
        message = findViewById(R.id.dummy_text3);
        button = findViewById(R.id.dummy_send);
        okHttpClient = new OkHttpClient();

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String coordX = X.getText().toString();
                String coordY = Y.getText().toString();
                String msg = message.getText().toString();


                // we add the information we want to send in
                // a form. each string we want to send should
                // have a name. in our case we sent the
                // dummyText with a name 'sample'
                RequestBody formbody
                        = new FormBody.Builder()
                        .add("coordX", coordX)
                        .add("coordY", coordY)
                        .add("msg", msg)
                        .build();

                // while building request
                // we give our form
                // as a parameter to post()
                Request request = new Request.Builder().url("http://192.168.0.103:5000/debug")
                        .post(formbody)
                        .build();
                okHttpClient.newCall(request).enqueue(new Callback() {
                    @Override
                    public void onFailure(
                            @NotNull Call call,
                            @NotNull IOException e) {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(getApplicationContext(), "server down", Toast.LENGTH_SHORT).show();
                            }
                        });
                    }

                    @Override
                    public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                        if (response.body().string().equals("received")) {
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    Toast.makeText(getApplicationContext(), "data received", Toast.LENGTH_SHORT).show();
                                    X.setText("");
                                    Y.setText("");
                                    message.setText("");
                                }
                            });
                        }
                    }
                });
            }
        });

        BluetoothScanner bluetoothScanner =
                new EstimoteBluetoothScannerFactory(getApplicationContext()).getSimpleScanner();
        ScanHandler telemetryScanHandler =
                bluetoothScanner
                        .estimoteTelemetryFrameAScan() // or estimoteTelemetryFrameBScan
                        .withOnPacketFoundAction(new Function1<EstimoteTelemetryFrameA, Unit>() {
                            @Override
                            public Unit invoke(EstimoteTelemetryFrameA estimoteTelemetryFrameA) {
                                Log.d("TLM", "telemetry A detected: $it");
                                return null;
                            }
                        })
                        .withOnScanErrorAction(new Function1<Throwable, Unit>() {
                            @Override
                            public Unit invoke(Throwable throwable) {
                                Log.e("TLM", "scan failed: $it");
                                return null;
                            }
                        })
                        .start();
    }
}