import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:location/location.dart';
import 'package:geolocator/geolocator.dart';

import '../screens/bluetooth_off_screen.dart';
import '../screens/MainHomePage1.dart';
import '../screens/MainHomePage2.dart';

////////////////////  MainHomePage1 is call for control group app.
// //////////////// MainHomePage2 is for test group app.

void main() {
  FlutterBluePlus.setLogLevel(LogLevel.verbose, color: true);
  runApp(const FlutterBlueApp());
  //runApp(const MyApp());
}

class FlutterBlueApp extends StatefulWidget {
  const FlutterBlueApp({Key? key}) : super(key: key);

  @override
  State<FlutterBlueApp> createState() => _FlutterBlueAppState();
}

class _FlutterBlueAppState extends State<FlutterBlueApp> {
  BluetoothAdapterState _adapterState = BluetoothAdapterState.unknown;
  bool _isLocationServiceEnabled = false;

  late StreamSubscription<BluetoothAdapterState> _adapterStateSubscription;
  late StreamSubscription<ServiceStatus> _locationServiceStatusSubscription;
  late Location _location;

  @override
  void initState() {
    super.initState();
    _location = Location();

    // Listen to Bluetooth adapter state
    _adapterStateSubscription = FlutterBluePlus.adapterState.listen((state) {
      _adapterState = state;
      if (mounted) {
        setState(() {});
      }
    });

    // Listen to location service status changes using Geolocator
    _locationServiceStatusSubscription = Geolocator.getServiceStatusStream().listen((status) {
      _isLocationServiceEnabled = status == ServiceStatus.enabled;
      if (mounted) {
        setState(() {});
      }
    });

    // Check initial location service status using Location package
    _checkLocationServiceStatus();
  }

  Future<void> _checkLocationServiceStatus() async {
    bool serviceEnabled = await _location.serviceEnabled();
    if (!serviceEnabled) {
      //serviceEnabled = await _location.requestService();
      serviceEnabled = false;
    }
    setState(() {
      _isLocationServiceEnabled = serviceEnabled;
    });
  }

  void _toggleLocationService() async {
    bool serviceEnabled = await _location.serviceEnabled();
    if (!serviceEnabled) {
      serviceEnabled = await _location.requestService();
    } else {
      // No direct way to turn off location service programmatically
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please disable Location Service manually from settings.')),
      );
    }

    setState(() {
      _isLocationServiceEnabled = serviceEnabled;
    });
  }

  @override
  void dispose() {
    _adapterStateSubscription.cancel();
    _locationServiceStatusSubscription.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    Widget screen = _adapterState == BluetoothAdapterState.on && _isLocationServiceEnabled
        // ? const MainHomePage1(title: 'หน้าหลัก',)//YoutubeList()
        ? const MainHomePage2(title: 'หน้าหลัก',)//YoutubeList()
        : AdaptorsOffScreen(adapterState: _adapterState, adapterGPSState: _isLocationServiceEnabled);

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.light(
        //colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      // theme: ThemeData(
      //   colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      //   useMaterial3: true,
      // ),
      home: screen,
      navigatorObservers: [BluetoothAdapterStateObserver()],
    );

  }
}

class BluetoothAdapterStateObserver extends NavigatorObserver {
  StreamSubscription<BluetoothAdapterState>? _adapterStateSubscription;

  @override
  void didPush(Route route, Route? previousRoute) {
    super.didPush(route, previousRoute);
    if (route.settings.name == '/DeviceScreen') {
      // Start listening to Bluetooth state changes when a new route is pushed
      _adapterStateSubscription ??=
          FlutterBluePlus.adapterState.listen((state) {
            if (state != BluetoothAdapterState.on) {
              // Pop the current route if Bluetooth is off
              navigator?.pop();
            }
          });
    }
  }

  @override
  void didPop(Route route, Route? previousRoute) {
    super.didPop(route, previousRoute);
    // Cancel the subscription when the route is popped
    _adapterStateSubscription?.cancel();
    _adapterStateSubscription = null;
  }
}

// class MyApp extends StatelessWidget {
//   const MyApp({Key? key}) : super(key: key);
//
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'Flutter Demo',
//       theme: ThemeData(
//         primarySwatch: Colors.blue,
//       ),
//       home: const HomePage(),
//     );
//   }
// }
//
// class HomePage extends StatefulWidget {
//   const HomePage({Key? key}) : super(key: key);
//   @override
//   _HomePageState createState() => _HomePageState();
// }
//
// class _HomePageState extends State<HomePage> {
//   // make all of them instance variable
//   late String dropdownValue = 'one';
//   late SharedPreferences prefs;
//   final _key = 'cur_r';
//
//   @override
//   void initState() {
//     super.initState();
//     _read(); // read in initState
//   }
//
//   _read() async {
//     prefs = await SharedPreferences.getInstance();
//     setState(() {
//       dropdownValue = prefs.getString(_key) ?? ''; // get the value
//     });
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(title: Text("AAA")),
//       body: Center(
//         child: DropdownButton<String>(
//           value: dropdownValue,
//           onChanged: (String? newValue) {
//             setState(() {
//               dropdownValue = newValue!;
//               prefs.setString(_key, dropdownValue); // save value to SharedPreference
//             });
//
//           },
//           items: ['one', 'two', 'three'].map((String value) {
//             return DropdownMenuItem<String>(
//               value: value,
//               child: Text(value),
//             );
//           }).toList(),
//         ),
//       ),
//     );
//   }
// }