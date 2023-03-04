package com.example.receiver.fragments;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

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
        myWebView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                super.onReceivedError(view, request, error);
                // Handle error loading webpage
                AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
                builder.setTitle("Serveur introuvable");
                builder.setMessage("Le serveur local n'est pas démarré ou l'URL est erronée.\n\nAccéder à l'onglet 'Settings' pour modifier l'URL");
                builder.setPositiveButton("D'accord", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        // do nothing
                    }
                });
                builder.show();
            }
        });

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