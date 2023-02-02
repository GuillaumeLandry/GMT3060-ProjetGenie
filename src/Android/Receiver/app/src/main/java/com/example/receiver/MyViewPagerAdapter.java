package com.example.receiver;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.viewpager2.adapter.FragmentStateAdapter;

import com.example.receiver.fragments.Settings;
import com.example.receiver.fragments.Toggle;
import com.example.receiver.fragments.Webview;

public class MyViewPagerAdapter extends FragmentStateAdapter {

    public MyViewPagerAdapter(@NonNull FragmentActivity fragmentActivity) {
        super(fragmentActivity);
    }

    @NonNull
    @Override
    public Fragment createFragment(int position) {
        switch (position) {
            case 0:
                return new Toggle();
            case 1:
                return new Webview();
            case 2:
                return new Settings();
            default:
                return new Toggle();
        }
    }

    @Override
    public int getItemCount() {
        return 3;
    }
}
