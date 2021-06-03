# Moonsense Cloud API Client

Simple client library for the Moonsense Cloud API.

# Installation

Install the module from PyPI: 

```shell
pip install moonsense 
```

Or from source like this:

```shell
python setup.py install 
```

# Getting Started

Start by getting an API secret key by navigating to Settings in the Console:

https://console.moonsense.cloud/dashboard

We recommend exporting the API secret key as an environment variable:

    export MOONSENSE_SECRET_TOKEN=...

You can then very easily list sessions and access the granular data:

```python
from moonsense.client import Client

client = Client()
for session in client.list_sessions():
    print(session)

    for bundle in client.read_session(session.session_id):
        # Each bundle is a SealedBundle. See schema below.

```

**Recommended:** For a more realistic example see [consumer_example.py](https://github.com/moonsense/python-sdk/blob/main/consumer_example.py). It shows how you can write a consumer that will process session data using an incremental approach.


# Schemas

**Important Note:** int64 fields are serialized as strings ([why?](https://github.com/protocolbuffers/protobuf/issues/2679))

The granular sensor data Bundles are stored as one JSON document per line with the following structure:

```protobuf
message SealedBundle {
        
    // The bundle as received from the mobile device
    bundle.Bundle bundle = 1;

    // Application ID that was the source of the data
    string app_id = 2;

    // Credential ID associated with the app
    string credential_id = 3;

    // Session ID for a specific recording
    string session_id = 4;

    // Plaintext User ID
    string user_id = 5;

    // The server time in millis when the bundle received
    int64 server_time_millis = 6;
}
```

A Bundle is a container for mobile device sensor data. All fields are optional and its up to the client to decide what data to collect and send and at what frequency.

```protobuf
message Bundle {

    repeated Location location_data = 1;

    repeated Accelerometer accelerometer_data = 2;

    repeated Magnetometer magnetometer_data = 3;

    repeated Gyroscope gyroscope_data = 4;

    // The time when the bundle was constructed on the device
    Clock client_time = 5;

    Battery battery = 6;

    repeated Activity activity_data = 7;

    repeated Orientation orientation_data = 8;

    repeated Temperature temperature_data = 9;

    repeated Light light_data = 10;

    repeated Pressure pressure_data = 11;

    repeated Humidity humidity_data = 12;

    repeated Steps steps_data = 13;

    repeated HeartRate heart_rate_data = 14;
}
```

Location Data Schema:

```protobuf
message Location {
    // Client side time when this location was determined (milliseconds since epoch)
    int64 determined_at = 1;

    // The estimated horizontal accuracy of this location, radial, in meters
    float horizontal_accuracy = 2;

    // The estimated vertical accuracy of this location, radial, in meters
    float vertical_accurracy = 3;

    // Altitude in meters above the WGS 84 reference ellipsoid
    double altitude = 4;

    // Bearing in degrees
    float bearing = 5;

    // The estimated bearing accuracy of this location, in degrees
    float bearing_accuracy_degrees = 6;

    // Latitude, in degrees
    double latitude = 7;

    // Longitude, in degrees
    double longitude = 8;

    // The provider of this location data
    string provider = 9;

    // Speed if it is available, in meters/second over ground
    float speed = 10;

    // The estimated accuracy of the speed
    float speed_accurracy = 11;
}
```

Accelerometer Data Schema:

```protobuf
message Accelerometer {
    // Client side time when this Accelerometer datapoint was determined (milliseconds since epoch)
    int64 determined_at = 1;

    // X-axis acceleration in G's (gravitational force).
    double x = 2;

    // Y-axis acceleration in G's (gravitational force).
    double y = 3;

    // Z-axis acceleration in G's (gravitational force).
    double z = 4;
}
```

Magnetometer Data Schema:

```protobuf
message Magnetometer {
    // Client side time when this Magnetometer datapoint was determined (milliseconds since epoch)
    int64 determined_at = 1;

    // X-axis magnetic field in micro-Tesla (uT).
    double x = 2;

    // Y-axis magnetic field in micro-Tesla (uT).
    double y = 3;

    // Z-axis magnetic field in micro-Tesla (uT).
    double z = 4;

    // Related documentation:
    // https://developer.android.com/reference/android/hardware/GeomagneticField
}
```

Gyroscope Data Schema:

```protobuf
message Gyroscope {
    // Client side time when this Gyroscope datapoint was determined (milliseconds since epoch)
    int64 determined_at = 1;

    // Rotation can be positive or negative.
    // X-axis acceleration in radians per second.
    double x = 2;

    // Y-axis acceleration in radians per second.
    double y = 3;

    // Z-axis acceleration in radians per second.
    double z = 4;
}
```

Client Clock Schema:

```protobuf
// Modeled after the Android SystemClock
// https://developer.android.com/reference/android/os/SystemClock
//
// Neither Android, nor iOS provide a trusted time source. The best we
// can do is record monotonic and non-monotonic time coordinates.
message Clock {

    // Standard wall clock (time and date) expressed in milliseconds since the epoch
    // This is controlled by the user or the phone network and it may jump backwards
    // or forwards unpredictably. This clock should only be used when correspondence
    // with real-world dates and times is important
    //
    // Android: System.currentTimeMillis()
    // iOS: NSDate()
    //
    int64 wall_time_millis = 1;

    // This clock MUST be guaranteed to be monotonic, and is suitable for interval timing
    // when the interval does not span device sleep. This clock stops when the system enters
    // deep sleep (CPU off, display dark, device waiting for external input), but is not 
    // affected by clock scaling, idle, or other power saving mechanisms.
    //
    // Android: SystemClock.uptimeMillis()
    // iOS: CACurrentMediaTime() which calls mach_absolute_time()
    //
    // Caveats regarding CACurrentMediaTime():
    // - https://bendodson.com/weblog/2013/01/29/ca-current-media-time/
    //
    int64 timer_millis = 2;

    // This clock MUST be monotonic, and needs to continue to tick even when the CPU is in
    // power saving modes, so is the recommend basis for general purpose interval timing.
    //
    // Android: SystemClock.elapsedRealtime()
    // iOS: ProcessInfo.processInfo.systemUptime
    // (see https://forums.swift.org/t/recommended-way-to-measure-time-in-swift/33326)
    //
    int64 timer_realtime_millis = 3;
}
```

Battery Data Schema:

```protobuf
message Battery {
    enum State {
        UNKNOWN = 0;
        CHARGING = 1;
        DISCHARGING = 2;
        FULL = 3;
    }

    // Remaining battery capacity as an integer percentage of total capacity (with no fractional part).
    int32 capacity = 1;

    // Current battery state (discharging, charging or full)
    State state = 2;
}
```

Activity Data Schema:

```protobuf
message Activity {
    enum Type {
        UNKNOWN = 0;
        IN_VEHICLE = 1;
        ON_BICYCLE = 2;
        ON_FOOT = 3;
        RUNNING = 4;
        STILL = 5;
        TILTING = 6;
        WALKING = 7;
    }

    // Client side time when this activity was determined (milliseconds since epoch)
    int64 determined_at = 1;

    Type type = 2;

    // A value from 0 to 100 indicating the likelihood that the user is performing this activity.
    int32 confidence = 3;
}
```

Orientation Data Schema:

```protobuf
message Orientation {
    // Client side time when this orientation was determined (milliseconds since epoch)
    int64 determined_at = 1;

    // Angle of rotation about the -z axis. This value represents the angle between the device's y 
    // axis and the magnetic north pole. When facing north, this angle is 0, when facing south, this
    // angle is π. Likewise, when facing east, this angle is π/2, and when facing west, this angle 
    // is -π/2. The range of values is -π to π.
    float azimuth = 2;

    // Angle of rotation about the x axis. This value represents the angle between a plane parallel
    // to the device's screen and a plane parallel to the ground. Assuming that the bottom edge of
    // the device faces the user and that the screen is face-up, tilting the top edge of the device
    // toward the ground creates a positive pitch angle. The range of values is -π to π.
    float pitch = 3;

    // Angle of rotation about the y axis. This value represents the angle between a plane perpendicular
    // to the device's screen and a plane perpendicular to the ground. Assuming that the bottom edge of
    // the device faces the user and that the screen is face-up, tilting the left edge of the device toward
    // the ground creates a positive roll angle. The range of values is -π/2 to π/2.
    float roll = 4;
}
```

Temperature Data Schema:

```protobuf
message Temperature {
    // Client side time when this value was determined (milliseconds since epoch)
    int64 determined_at = 1;

    // Ambient air temperature. Unit: °C
    float value = 2;
}
```

Light Data Schema:

```protobuf
message Light {
    // Client side time when this value was determined (milliseconds since epoch)
    int64 determined_at = 1;

    // Ambient illuminance. Unit: lx
    float value = 2;
}
```

Pressure Data Schema:

```protobuf
message Pressure {
    // Client side time when this value was determined (milliseconds since epoch)
    int64 determined_at = 1;

    // Ambient air pressure. Unit: mbar
    float value = 2;
}
```

Humidity Data Schema:

```protobuf
message Humidity {
    // Client side time when this value was determined (milliseconds since epoch)
    int64 determined_at = 1;

    // Ambient relative humidity. Unit: % (percentage)
    float value = 2;
}
```

Steps Data Schema:

```protobuf
message Steps {
    int32 count = 1;

    // Client side time that represents the start of the interval
    // over which this value was computed (milliseconds since epoch)
    int64 from = 2;

    // Client side time that represents the end of the interval over
    // which this value was computed (milliseconds since epoch)
    int64 to = 3;
}
```

Heart Rate Data Schema:

```protobuf
message HeartRate {
    int32 rate = 1;

    // Client side time that represents the start of the interval over
    // which this value was computed (milliseconds since epoch)
    int64 from = 2;

    // Client side time that represents the end of the interval over
    // which this value was computed (milliseconds since epoch)
    int64 to = 3;
}
```

# Tests

Simply run: `pytest`

# Code coverge

Generate coverage report with: `py.test --cov=moonsense tests/`
