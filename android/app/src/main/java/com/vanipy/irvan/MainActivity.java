package com.vanipy.irvan;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/**
 * The whole app is the offline "world map" from irvan's index.html, bundled as
 * a WebView asset. Pinch to zoom, drag to pan, tap a place for its card.
 * Links in a card open in the browser app, never inside the map, so the app
 * itself needs no network permission.
 */
public class MainActivity extends Activity {
    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true); // pan/zoom and the detail cards are script-driven
        s.setSupportZoom(true);
        s.setBuiltInZoomControls(true);
        s.setDisplayZoomControls(false); // pinch only, no on-screen buttons
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true); // start fit-to-screen
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if ("file".equals(uri.getScheme())) {
                    return false; // the bundled map itself
                }
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, uri));
                } catch (Exception ignored) {
                    // no browser installed: the link simply does nothing
                }
                return true;
            }
        });
        setContentView(web);
        web.loadUrl("file:///android_asset/map.html");
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) {
            web.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
