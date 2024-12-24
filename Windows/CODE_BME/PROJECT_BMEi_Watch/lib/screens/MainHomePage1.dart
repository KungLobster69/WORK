import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:youtube_metadata/youtube_metadata.dart';
import 'package:transparent_image/transparent_image.dart';
import 'setting.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'youtube_exercise_list.dart';
import 'youtube_learn_list.dart';
import '../utils/BLEConnect.dart';
import '../utils/snackbar.dart';

class MainHomePage1 extends StatefulWidget {
  const MainHomePage1({super.key, required this.title});
  final String title;

  @override
  _MainHomePage1State createState() => _MainHomePage1State();

}

class _MainHomePage1State extends State<MainHomePage1> {
  final menuName = <String>[
  'ความรู้การป้องกัน  covid', 'การฝึกหายใจและยืดกล้ามเนื้อ', 'การออกกำลังกาย', 'รายงานอาการไม่พึงประสงค์ (ถ้ามี)',
  ];

  final assetName = <String>[
    'assets/images/COVID19.png', 'assets/images/Breath_Stretch.png', 'assets/images/Exercises.png', 'assets/images/Patient_Report.png',
  ];

  late String savedText1;
  late String savedText2;

  late BLEConnect myBLE = BLEConnect();

  @override
  void initState() {
    super.initState();
    loadConfig(); // Call fetchData() to load the data
  }

  void refreshPage() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("ค้นหาอุปกรณ์ รอสักครู่..."),backgroundColor: Colors.green),
    );
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const MainHomePage1(title: "หน้าหลัก")),
    );
  }

  Future<void> loadConfig() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    savedText1 = prefs.getString('user_input_key1') ?? '';
    savedText2 = prefs.getString('user_input_key2') ?? '';

    setState(() {
      print('function_load');
      print(savedText1);
      print(savedText2);

      if (savedText1 == '' || savedText2 == '') {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => HomePagesetting()),
        ).then((value) {
          // คำสั่งที่จะทำงานหลังจากการ pop
          print('Returned from HomePagesetting');
          // myBLE = BLEConnect();
          myBLE.startBluetoothConnectionfinger(context); // Pass the context here
        });
      }else{
        //myBLE = BLEConnect();
        myBLE.startBluetoothConnectionfinger(context); // Pass the context here
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title, style: TextStyle(fontSize: 18)),
        backgroundColor: Colors.greenAccent[100],
        leading: Image.asset('assets/images/BMEi.png'),
        actions: <Widget>[
          IconButton(
            icon: const Icon(
              Icons.search_outlined,
              color: Colors.white,
            ),
            onPressed: refreshPage,
          ),
          IconButton(
              icon: const Icon(
                Icons.settings,
                color: Colors.white,
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => HomePagesetting()),
                ).then((value) {
                  // คำสั่งที่จะทำงานหลังจากการ pop
                  print('Returned from MyHomePagesetting');
                  // myBLE = BLEConnect();
                  myBLE.startBluetoothConnectionfinger(context);

                  //startBluetoothConnectionpush();
                });
              }
          ),
        ],
      ),
      body: Stack(
        children: [
          Positioned.fill(
              child:
                Image.asset("assets/images/AMS_BMEI.png",
                fit: BoxFit.contain,
              ),
          ),
          SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 24.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: List.generate(menuName.length, (index) => _buildCard(index,menuName[index],assetName[index])), // Generates 5 cards
              ),
          ),
        ],
      ),
    );
  }

  Widget _buildCard(int index, String menuName, String assetName) {
    return Card(
      margin: const EdgeInsets.all(10),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(8.0))),
      color: Colors.white60,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Stack(
            alignment: Alignment.center,
            children: <Widget>[
              GestureDetector(
                onTap: () {
                  if(index == 0 || index == 1){
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => YoutubeLearnList(reasonIndex: index)),
                    );
                  }else if (index == 2){
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => YoutubeExerciseList()),
                    );
                  }else{
                    // Navigator.push(
                    //   context,
                    //   MaterialPageRoute(builder: (context) => YoutubeList()),
                    // );
                  }

                },
                  child: ClipRRect(
                    // borderRadius: BorderRadius.all(Radius.circular(8.0)),
                    borderRadius: const BorderRadius.only(
                      topLeft: Radius.circular(8.0),
                      topRight: Radius.circular(8.0),
                    ),
                    child: Image.asset(
                      assetName,
                      fit: BoxFit.scaleDown,
                    ),
                ),
              ),

              // GestureDetector(
              //   onTap: () {
              //     // Action when card is tapped
              //   },
              //   child: const CircleAvatar(
              //     radius: 30,
              //     backgroundColor: Colors.black45,
              //     child: Icon(
              //       Icons.play_arrow,
              //       size: 40,
              //       color: Colors.white,
              //     ),
              //   ),
              // ),
            ],
          ),
          ListTile(
            title: Center(
              child: Text(
                menuName,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}