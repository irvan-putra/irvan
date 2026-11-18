package com.vanipy.irvan;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import android.view.ViewGroup;
import android.webkit.WebView;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.Robolectric;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.annotation.Config;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.regex.Pattern;

@RunWith(RobolectricTestRunner.class)
@Config(sdk = 34)
public class MapAssetTest {

    private static String readAsset(MainActivity activity, String name) throws Exception {
        try (InputStream in = activity.getAssets().open(name)) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[8192];
            int n;
            while ((n = in.read(buf)) != -1) {
                out.write(buf, 0, n);
            }
            return new String(out.toByteArray(), StandardCharsets.UTF_8);
        }
    }

    @Test
    public void mapAssetIsTheWorldMap() throws Exception {
        MainActivity activity = Robolectric.buildActivity(MainActivity.class).get();
        String html = readAsset(activity, "map.html");
        assertTrue("asset must contain the world map svg",
                Pattern.compile("<svg id=\"map\" viewBox=\"0 0 1200 860\"").matcher(html).find());
        assertTrue("the plaza photo must be embedded so the map works offline",
                html.contains("data:image/png;base64,"));
        assertFalse("asset must stay offline: no external scripts",
                html.contains("<script src"));
        assertFalse("asset must stay offline: no runtime fetches",
                html.contains("fetch(") || html.contains("XMLHttpRequest"));
        assertFalse("asset must stay offline: no external images or styles",
                html.contains("src=\"http") || html.contains("url(http"));
        // plain anchor hrefs (the source link, the data-table link chips) are
        // inert offline; the app opens them in the browser app on tap, so they
        // are the only URLs allowed
    }

    @Test
    public void activityShowsBundledMapWithPinchZoom() {
        MainActivity activity = Robolectric.buildActivity(MainActivity.class).create().get();
        ViewGroup root = (ViewGroup) activity.findViewById(android.R.id.content);
        WebView web = (WebView) root.getChildAt(0);
        assertNotNull(web);
        assertTrue(web.getSettings().getJavaScriptEnabled());
        assertTrue(web.getSettings().getSupportZoom());
        assertTrue(web.getSettings().getBuiltInZoomControls());
        assertFalse(web.getSettings().getDisplayZoomControls());
        assertTrue(web.getSettings().getUseWideViewPort());
        assertTrue(web.getSettings().getLoadWithOverviewMode());
    }
}
