package com.example.receiver.fragments;

import android.graphics.Color;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.ToggleButton;

import com.example.receiver.MainActivity;
import com.example.receiver.R;

public class Toggle extends Fragment {
    private ToggleButton btnToggle;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_toggle, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        view.setBackgroundColor(Color.RED);

        btnToggle = view.findViewById(R.id.btn_toggle_ble);
        btnToggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    enableBLE(view);
                } else {
                    disableBLE(view);
                }
            }
        });
    }

    private void enableBLE(View view) {
        view.setBackgroundColor(Color.GREEN);
        MainActivity.startScan();
    }

    private void disableBLE(View view) {
        view.setBackgroundColor(Color.RED);
        MainActivity.stopScan();
    }
}