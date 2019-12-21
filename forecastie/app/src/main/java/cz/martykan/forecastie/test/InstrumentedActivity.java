package cz.martykan.forecastie.test;

import android.util.Log;

import cz.martykan.forecastie.activities.MainActivity;

public class InstrumentedActivity extends MainActivity {
    public static String TAG = "IntrumentedActivity";
    private FinishListener mListener;
    public void setFinishListener(FinishListener listener) {
        mListener = listener;
    }
    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG + ".InstrumentedActivity", "onDestroy()");
        super.finish();
        if (mListener != null) {
            mListener.onActivityFinished();
        }
    }
}