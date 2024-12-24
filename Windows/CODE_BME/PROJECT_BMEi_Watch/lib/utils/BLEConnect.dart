import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'variables.dart' as globals;

class BLEConnect {
  BluetoothDevice? connectedDevicefinger;
  BluetoothCharacteristic? targetCharacteristicfinger;
  late String HNid;
  late String DeviceID;
  late String MacID;

  BLEConnect();
  String DeviceName = '';

  Future<void> startBluetoothConnectionfinger(BuildContext context) async {
    print('เข้าสู่การสแกนหา startBluetoothConnectionfinger');

    Map<Permission, PermissionStatus> statuses = await [
      Permission.storage,
      Permission.location
    ].request();

    await loadSavedText();
    await startScanning(context);
  }

  Future<void> startScanning(BuildContext context) async {
    bool deviceFound = false;
    try {
      await FlutterBluePlus.startScan(timeout: Duration(seconds: 5));

      FlutterBluePlus.onScanResults.listen((results) async {
        if (results.isNotEmpty) {
          ScanResult scanResult = results.last;
          //Scanning with Device name
          DeviceName = "BMEiWatch_" + globals.namedevice;
          if (scanResult.device.advName.toString().toLowerCase() == DeviceName.toLowerCase()){
            deviceFound = true;
            await FlutterBluePlus.stopScan();
            await _connectToDevice(scanResult, context);
          }
          //Scanning with Device mac address
          MacID = "e4:c1:f4:c9:c7:bb";
          if (scanResult.device.remoteId.toString() == MacID.toUpperCase()) {
            deviceFound = true;
            await FlutterBluePlus.stopScan();
            await _connectToDevice(scanResult, context);
          }
        }
      });

      // Wait for the scan to complete
      await Future.delayed(Duration(seconds: 5));

      if (!deviceFound) {
        // Show error Snackbar if the device is not found
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("ค้นหาและเชื่อมต่ออุปกรณ์ไม่สำเร็จ"),backgroundColor: Colors.red),
        );
      }
    } catch (e) {
      // Show error Snackbar if scanning fails
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error during scanning: ${e.toString()}")),
      );
    } finally {
      await FlutterBluePlus.stopScan(); // Ensure scanning stops
    }
  }

  Future<void> _connectToDevice(ScanResult scanResult, BuildContext context) async {
    try {
      print("กำลังเชื่อมต่อ");

      await scanResult.device.connect();

      connectedDevicefinger = scanResult.device;
      print("เชื่อมต่อสำเสร็จ");

      // Discover services and characteristics
      final services = await scanResult.device.discoverServices();
      final service = services[2]; // for BMEI Watch BLE, the service is at index 2
      final characteristicUuid = service.characteristics[1]; // for BMEI Watch BLE,the characteristic is at index 0, index 1 is for Oximeter

      await characteristicUuid.setNotifyValue(characteristicUuid.isNotifying == false);
      characteristicUuid.read();
      characteristicUuid.lastValueStream.listen((value) async {
        // print("Pulse: ${value[0]}"); //for BMEI Watch BLE
        // print("SpO2: ${0}"); //BMEI Watch BLE

        int pulseValue = value[3]; //index[3] for Oximeter and index[0] for BMEi Watch

        print("Pulse: $pulseValue"); //for Oximeter
        print("SpO2: ${value[4]}");  //for Oximeter

        if ((pulseValue.toInt() < 50) || (99 < 50)){
          globals.receivedDatafinger_PRbpm = 0;
          globals.receivedDatafinger_SpO2 = 0;
          globals.DataReadStatus = 'กรุณารอสักครู่';
        }else{
          globals.receivedDatafinger_PRbpm = pulseValue;
          globals.receivedDatafinger_SpO2 = 99;
          globals.DataReadStatus = 'กำลังวัดค่าและแสดงผล';
        }

      });

      // Show success Snackbar
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("ค้นหาและเชื่อมต่ออุปกรณ์สำเร็จ"),backgroundColor: Colors.blue),
      );
    } catch (e) {
      // Show error Snackbar if the connection fails
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Failed to connect: ${e.toString()}")),
      );
    }
  }

  Future<void> loadSavedText() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    HNid = prefs.getString('user_input_key1') ?? '';
    DeviceID = prefs.getString('user_input_key2') ?? '';

    globals.HNID = HNid;
    globals.namedevice = DeviceID;

  }

  Future<void> disconnect() async {
    await connectedDevicefinger!.disconnect();
    //await flutterBluefinger.stopScan();
  }

}
