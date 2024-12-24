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
import 'youtube_exercise_control1.dart';
import 'youtube_exercise_control2.dart';
import 'youtube_exercise_control3.dart';

class YoutubeExercisePage extends StatefulWidget {
  const YoutubeExercisePage({super.key});

  @override
  _YoutubeExercisePageState createState() => _YoutubeExercisePageState();

}

class _YoutubeExercisePageState extends State<YoutubeExercisePage> {
  final menuName = <String>[
    'การออกกำลังกล้ามเนื้อหายใจ', 'การออกกำลังแบบแอโรบิก', 'การออกกำลังแบบใช้แรงต้าน',
  ];

  final assetName = <String>[
    'assets/images/HeartExercise.png', 'assets/images/AerobicExercise.png', 'assets/images/ResistanceExercise.png',
  ];

  late String savedText1;
  late String savedText2;

  late BLEConnect myBLE = BLEConnect();

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("ชุดการออกกำลังกาย", style: TextStyle(fontSize: 18)),
        backgroundColor: Colors.greenAccent[100],
        leading: Image.asset('assets/images/BMEi.png'),
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
                  if(index == 0){
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => YoutubeControlList1()),
                    );
                  }else if (index == 1){
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => YoutubeControlList2()),
                    );
                  }else if (index == 2){
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => YoutubeControlList3()),
                    );
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