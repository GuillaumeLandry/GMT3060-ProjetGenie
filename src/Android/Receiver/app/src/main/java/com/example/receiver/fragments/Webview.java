package com.example.receiver.fragments;

import android.annotation.SuppressLint;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;

import com.example.receiver.MainActivity;
import com.example.receiver.R;

public class Webview extends Fragment {
    WebView myWebView;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View myView = inflater.inflate(R.layout.fragment_webview, container, false);

        myWebView = myView.findViewById(R.id.webView);
        myWebView.loadUrl(MainActivity.getURL());
        WebSettings webSettings = myWebView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setUserAgentString("AndroidReceiver");

        // Inflate the layout for this fragment
        return myView;
    }

    @Override
    public void onResume() {
        super.onResume();
        if (!myWebView.getUrl().equals(MainActivity.getURL())) {
            myWebView.loadUrl(MainActivity.getURL());
        }
    }
}