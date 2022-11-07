package com.estimote.blank;

import android.app.Application;

import com.estimote.proximity_sdk.api.EstimoteCloudCredentials;

//
// Running into any issues? Drop us an email to: contact@estimote.com
//

public class MyApplication extends Application {

    EstimoteCloudCredentials estimoteCloudCredentials =
            new EstimoteCloudCredentials("universal-template-4r8", "697ce7ec7ffb494e88d6c782a698b95e");

}
