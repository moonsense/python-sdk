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

Start by getting an API secret key by navigating to App in Console and creating a token. You will need to save the generated secret key to a secure place.

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

# Webhooks

See [webhook_example.py](https://github.com/moonsense/python-sdk/blob/main/webhook_example.py) for an example on how to create a very simple handler that the consumer webhooks.

The request payload use the following schema:

```protobuf
 message WebhookPayload {
    string project_id = 1; // checked in the handler since not all event types can provide a projectId.
    string app_id = 2;
    string session_id = 3;
    WebhookEventTypes event_type = 4;
    v2.bundle.SealedBundle bundle = 5; // payload is optional and only a small number of events require a bundle.
    string client_session_group_id = 6;
    repeated string session_labels = 7;
}
```

The following webhook types are supported:

```protobuf
enum WebhookEventTypes {
    UNKNOWN = 0;
    SESSION_CREATED = 1;
    BUNDLE_RECEIVED = 2;
    CHUNK_PERSISTED = 3;
    SESSION_INACTIVE = 4;
}
```

# Schemas

**Important Note:** int64 fields are serialized as strings ([why?](https://github.com/protocolbuffers/protobuf/issues/2679))

The granular sensor data Bundles are stored as one JSON document per line with the following structure:

```protobuf
message SealedBundle {

    // The bundle as received in the BundleEnvelope
    Bundle bundle = 1;

    // Application ID that was the source of the data
    string app_id = 2;

    // Credential ID associated with the app
    string credential_id = 3;

    // Session ID for a specific recording
    string session_id = 4;

    // Plaintext User ID
    string user_id = 5;

    // The server time in millis when the bundle envelope was constructed
    int64 server_time_millis = 6;

    // Unique install ID generated by the OS.
    string install_id = 7;

    // User is provided by the client as it becomes available (e.g after customer authenticates an user).
    string client_user_id = 8;
}
```

A Bundle is a container for mobile device sensor data. All fields are optional and its up to the client to decide what data to collect and send and at what frequency.

```protobuf
message Bundle {

    repeated Location location_data = 1;

    repeated Accelerometer accelerometer_data = 2;

    repeated Magnetometer magnetometer_data = 3;

    repeated Gyroscope gyroscope_data = 4;

    // The time when the bundle was constructed
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

    repeated Pointer pointer_data = 15;

    // Device acceleration without the gravity component
    repeated Accelerometer linear_accelerometer_data = 16;

    repeated Marker markers = 17;

    // Continuous monotonic increasing index generated by the client
    int32 index = 18;

    repeated TextChange text_change_data = 19;

    repeated KeyPress key_press_data = 20;

    repeated FocusChange focus_change_data = 21;
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

Pointer Data Schema:

```protobuf
message Pointer {
    enum Type {
        UNKNOWN = 0;
        STYLUS = 1;
        INVERTED_STYLUS = 2;
        TOUCH = 3;
        MOUSE = 4;
    }

    // Pointer events operate in the coordinate space of the screen, 
    // scaled to logical pixels.  Logical pixels approximate a grid with 
    // about 38 pixels per centimeter, or 96 pixels per inch.

    // This allows analysis be performed independent of the precise hardware
    // characteristics of the device. In particular, features such as touch 
    // slop can be defined in terms of roughly physical lengths so that
    // the user can shift their finger by the same distance on a high-density 
    // display as on a low-resolution device.

    // Time of event dispatch in milliseconds, relative to an arbitrary timeline.
    int64 determined_at = 1;

    // The type of the pointer event that was used.
    Type type = 2;

    // Bit field calculated using a bitwise AND operation over constants
    // that represent individual buttons on a device.
    int64 buttons = 3;

    // Distance in logical pixels that the pointer moved since the last data point. Note
    // that the delta is reported per gesture. The delta values reset when a new gesture
    // is started.
    Offset2D delta = 4;

    // Unique identifier for the pointing device. Note that all platforms iOS, Android
    // and Web report a new device id for each new gesture. The device can be used as
    // a logical grouping of Pointer events that belong to a particular gesture.
    int64 device = 5;

    // The distance of the detected object from the input surface.
    double distance = 6;

    // The range of possible values for distance.
    ClosedRange distance_range = 7;

    // Set if an application from a different security domain is in any way
    // obscuring this application's window. Note that this field is not implemented
    // as there is no means of deriving this information on all platforms.
    bool obscured = 8 [deprecated = true];

    // The orientation angle of the detected object, in radians.
    double orientation = 9;

    // Coordinate of the position of the pointer, in logical pixels in the global coordinate space.
    Offset2D position = 10;

    // The pressure of the touch.
    double pressure = 11;

    // The range of possible values for pressure.
    ClosedRange pressure_range = 12;

    // The radius of the contact ellipse along the major axis, in logical pixels.
    double radius_major = 13;

    // The radius of the contact ellipse along the minor axis, in logical pixels.
    double radius_minor = 14;

    // The range of possible values of radius;
    ClosedRange radius_range = 15;

    // The area of the screen being pressed.
    double size = 16;

    // Set if the event was generated by some automated mechanism.
    bool synthesized = 17;

    // The tilt angle of the detected object, in radians.
    double tilt = 18;

    // Set if the touch was detected to have come from a software keyboard.
    bool is_software_keyboard = 19;
}
```

Text Change Schema:

```protobuf
// Represents a message that is fired everytime a text change
// event happens on a specified input target.
message TextChange {
    enum Action {
        UNKNOWN = 0;    // Encompasses all the other types of text change events
                        // including typing, swipe, autofill, autocomplete. Essentially
                        // anything that is not cut or paste.
        CUT = 1;
        PASTE = 2;
    }

    // Time of event dispatch in milliseconds, relative to an arbitrary timeline.
    int64 determined_at = 1;

    // Represents the target input field that detected the text change event.
    TargetElement target = 2;

    // This value represents whether the input field represented by target(see above)
    // is in focus or not.
    bool focus = 3;

    // Provides a snapshot of the text contained in the input field represented by the target
    // at the determined time. Note that the caller can infer the characters typed based on
    // how this text changes over time. For privacy purposes this string
    // is masked and does not correspond to the actual characters typed.
    string masked_text = 4;

    // Returns true if the captured text exceeds the maximum allowable limit. In
    // cases like these the text is truncated and this flag returns a true.
    bool truncated_text = 5;

    // Determines if the text change was a result of a specific action.
    Action action = 6;
}
```

Key Press Schema:

```protobuf
message KeyPress {
    enum Type {
        UNKNOWN = 0;
        KEY_UP = 1;
        KEY_DOWN = 2;
    }

    // Time of event dispatch in milliseconds, relative to an arbitrary timeline.
    int64 determined_at = 1;

    // The type of key event that was detected.
    Type type = 2;

    // Provides a string value for a special, logical or modifier key
    // that was pressed, for eg. 'Home', 'Left Shift' etc.
    // The value reflects the actual key that was pressed and is therefore not masked.
    // There is a possibility that the value returned by this field differs
    // across platforms.
    string special_key = 3;

    // The unicode value for the key pressed. This field is masked for privacy
    // reasons and does not correspond to the exact key that was pressed.
    // The pressed key is guaranteed to be a unicode character. Defaults to
    // '0' if unavailable.
    int32 masked_key = 4;

    // Represents the target field that detected the key event.
    TargetElement target = 5;

    // Flag to specify the event as including an 'Alt Key'
    bool alt_key = 6;

    // Flag to specify the event as including an 'Control (Ctrl) Key'
    bool control_key = 7;

    // Flag to specify the event as including an 'Meta Key'.
    // This includes the Windows Key (⊞) on windows and the Command Key (⌘) on MacOS
    bool meta_key = 8;

    // Flag to specify the event was captured while the 'Shift' Key
    // was active
    bool shift_key = 9;
}
```

Focus Change Schema:

```protobuf
message FocusChange {
    enum Type {
        UNKNOWN = 0;
        FOCUS_GAINED = 1;
        FOCUS_LOST = 2;
    }

    // Time of event dispatch in milliseconds, relative to an arbitrary timeline.
    int64 determined_at = 1;

    // The type of focus event that was detected.
    Type type = 2;

    // Represents the target field that detected the key event.
    TargetElement target = 3;
}
```

A target element is defined like this:

```protobuf
message TargetElement {
    // A unique identifier that represents an element that is being interacted
    // with. The id is guaranteed to be different for each element in the
    // application. The SDK makes the best effort to ensure the consistency of
    // this id. The user can override this value by providing their own id.
    string target_id = 1;

    // This type data accompanies the target_id. The SDK makes a best
    // attempt at determining the type of the target based on
    // the properties of the element. The user can override this
    // value by providing their own type.
    string target_type = 2;
}
```

# Tests

Simply run: `pytest`

# Release

```bash
rm -rf build/ dist/
python setup.py sdist bdist_wheel
twine upload dist/*
```

Dont' forget to bump main branch to the next version.

# Code coverge

Generate coverage report with: `py.test --cov=moonsense tests/`
