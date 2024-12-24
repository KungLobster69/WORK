import 'dart:io';
import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:geolocator/geolocator.dart';
import 'package:location/location.dart';

import '../utils/snackbar.dart';


class AdaptorsOffScreen extends StatelessWidget {
  AdaptorsOffScreen({Key? key, this.adapterState, required this.adapterGPSState}) : super(key: key);

  final BluetoothAdapterState? adapterState;
  final bool adapterGPSState;

  final Location _location = Location();
  late bool _isLocationServiceEnabled = false;

  Widget buildAdapterOffIcon(BuildContext context, {required IconData setIcon}) {
     return Icon(
       setIcon,
      size: 100.0,
      color: Colors.white70,
    );
  }

  Widget buildTitle(BuildContext context, {required String adapterTitle}) {
    String? state = adapterState?.toString().split(".").last;
    return Text(
      '$adapterTitle Adapter is ${state != null ? state : 'not available'}',
      style: Theme.of(context).primaryTextTheme.titleSmall?.copyWith(color: Colors.white),
    );
  }

  Widget buildTitle1(BuildContext context, {required String adapterTitle}) {
    String? state = adapterGPSState?.toString().split(".").last;
    if (state == "true"){
      state = 'on';
    }else{
      state = 'off';
    }
    return Text(
      '$adapterTitle Adapter is ${state != null ? state : 'not available'}',
      style: Theme.of(context).primaryTextTheme.titleSmall?.copyWith(color: Colors.white),
    );
  }

  Future<void> _checkLocationServiceStatus() async {
    bool serviceEnabled = await _location.serviceEnabled();
    if (!serviceEnabled) {
      serviceEnabled = await _location.requestService();
      //serviceEnabled = await Geolocator.openLocationSettings();
    }
    _isLocationServiceEnabled = serviceEnabled;
    // setState(() {
    //
    // });
  }

  Widget buildGPSTurnOnButton(BuildContext context) {

    //final Location location = new Location();
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: ElevatedButton(
        child: const Text('TURN ON'),
        onPressed: () async {
          try {
            if (Platform.isAndroid) {
              _checkLocationServiceStatus();
              //await _location.requestService(); //use location flutter package
              //await Geolocator.openLocationSettings(); //use geolocator flutter packge
            }
          } catch (e) {
            Snackbar.show(ABC.a, prettyException("Error Turning On:", e), success: false);
          }
        },
      ),
    );
  }

  Widget buildBlueToothTurnOnButton(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: ElevatedButton(
        child: const Text('TURN ON'),
        onPressed: () async {
          try {
            if (Platform.isAndroid) {
              await FlutterBluePlus.turnOn();
            }
          } catch (e) {
            Snackbar.show(ABC.a, prettyException("Error Turning On:", e), success: false);
          }
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return ScaffoldMessenger(
      key: Snackbar.snackBarKeyA,
      child: Scaffold(
        backgroundColor: Colors.lightBlue,
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  buildAdapterOffIcon(context, setIcon: Icons.bluetooth_disabled),
                  Column(
                    children: [
                      if (Platform.isAndroid) buildBlueToothTurnOnButton(context),
                      buildTitle(context, adapterTitle: 'BlueTooth'),
                    ],
                  ),
                ],
              ),
              SizedBox(
                height:20
              ),
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  buildAdapterOffIcon(context,setIcon: Icons.location_disabled),
                  Column(
                    children: [
                      if (Platform.isAndroid) buildGPSTurnOnButton(context),
                      buildTitle1(context, adapterTitle: 'Location'),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class LocationService {
  Location location = Location.instance;

  Future<bool> requestPermission() async {
    final permission = await location.requestPermission();
    return permission == PermissionStatus.granted;
  }

  Future<LocationData> getCurrentLocation() async {
    final serviceEnabled = await location.serviceEnabled();
    if (!serviceEnabled) {
      final result = await location.requestService;
      if (result == true) {
        log('Service has been enabled');
      } else {
        throw Exception('GPS service not enabled');
      }
    }

    final locationData = await location.getLocation();
    return locationData;
  }
}
