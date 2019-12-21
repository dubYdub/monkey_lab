package cz.martykan.forecastie.test;

public interface FinishListener {
    void onActivityFinished();
    void dumpIntermediateCoverage(String filePath);
}