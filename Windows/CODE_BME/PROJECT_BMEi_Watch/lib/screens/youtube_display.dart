import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';
import 'package:csv/csv.dart';
import 'package:external_path/external_path.dart';
import 'dart:io';
import '../utils/ui.dart';
import '../utils/variables.dart' as globals;
import '../utils/BLEConnect.dart';
import 'youtube_exercise_list.dart' as goback;


class VideoPlayHR extends StatefulWidget {
  const VideoPlayHR({super.key, required this.videoURL, required this.videoTitle, required this.videoCaption});

  final String videoURL;
  final String videoTitle;
  final String videoCaption;
  // final BLEConnect BLECon;

  @override
  _VideoPlayHRState createState() => _VideoPlayHRState();
}

class _VideoPlayHRState extends State<VideoPlayHR> {
  late YoutubePlayerController _controller;
  bool isFullScreen = false;

  late PlayerState _playerState;
  late YoutubeMetaData _videoMetaData;
  double _volume = 100;
  bool _muted = false;
  bool _isPlayerReady = false;

  List<dynamic> dataList = [];

  Timer? _dataRecordingTimer; // Add a Timer variable

  @override
  void initState() {
    super.initState();
    final videoID = YoutubePlayer.convertUrlToId(widget.videoURL);

    globals.receivedDatafinger_PRbpm = 0;
    globals.receivedDatafinger_SpO2 = 0;
    globals.DataReadStatus = '';

    // Start Bluetooth connection
    //widget.BLECon.startBluetoothConnectionfinger(context);

    _controller = YoutubePlayerController(
      initialVideoId: videoID!,
      flags: const YoutubePlayerFlags(
        mute: false,
        autoPlay: true,
        disableDragSeek: true,
        loop: false,
        isLive: false,
        forceHD: true,
        enableCaption: false,
      ),
    )..addListener(_listener);

    _videoMetaData = const YoutubeMetaData();
    _playerState = PlayerState.unknown;

    _controller.addListener(() {
      if(_controller.value.isPlaying){
        _startDataRecording();
      }
      if (_controller.value.isFullScreen != isFullScreen) {
        setState(() {
          isFullScreen = _controller.value.isFullScreen;
        });
      }
    });
  }

  void _listener() {
    if (_isPlayerReady && mounted && !_controller.value.isFullScreen) {
      setState(() {
        _playerState = _controller.value.playerState;
        _videoMetaData = _controller.metadata;
      });
    }
  }

  @override
  void deactivate() {
    _controller.pause();
    super.deactivate();
  }

  @override
  void dispose() {
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight,
    ]);

    _dataRecordingTimer?.cancel();
    _controller.dispose();
    super.dispose();
  }

  // Start the timer for data recording
  void _startDataRecording() {
    if (_dataRecordingTimer == null || !_dataRecordingTimer!.isActive) {
      _dataRecordingTimer = Timer.periodic(Duration(seconds: 5), (timer) {
        data_recording();
      });
    }
  }

  void data_recording() async{
    DateTime now = DateTime.now();
    String date = now.day.toString().padLeft(2, '0');
    String month = now.month.toString().padLeft(2, '0');
    String year = now.year.toString();
    String hour = now.hour.toString().padLeft(2, '0');
    String minute = now.minute.toString().padLeft(2, '0');
    String second = now.second.toString().padLeft(2, '0');
    String nowday = "$date/$month/$year";
    String nowtime = "$hour:$minute:$second";
    if(globals.receivedDatafinger_PRbpm.toInt() == 0 || globals.receivedDatafinger_SpO2.toInt() == 0){
      // dataList = [
      //   {
      //     //"Date": nowday,
      //     "Time": nowtime,
      //     "Pulse": 0,
      //     "SpO2": 0
      //   }
      // ];
    }else{
      dataList = [
        {
          //"Date": nowday,
          "Time": nowtime,
          "Pulse": globals.receivedDatafinger_PRbpm,
          "SpO2": globals.receivedDatafinger_SpO2
        }
      ];
    }
    globals.csv_file_name = "$date-$month-$year-$hour-$minute-$second";
    List<dynamic> row = [];
    if (globals.header_added == false) {
      globals.header_added = true;
      globals.interval_sec = (now.second + globals.interval) % 60;
      //firstly, we once added a column header
      row.add(nowday);
      //row.add (globals.locationData);
      globals.associateLists!.add(row);
      //secondly, we once added more a column header
      row = [];
      row.add("Time");
      row.add("Pulse");
      row.add("SpO2");
      globals.associateLists!.add(row);
      //also, the first row data is recorded in a List at the staring time
      row = [];
      //row.add(dataList[0]["Date"]);
      row.add(dataList[0]["Time"]);
      row.add(dataList[0]["Pulse"]);
      row.add(dataList[0]["SpO2"]);
      globals.associateLists!.add(row);
    }else{
      globals.header_added = true;
      //recode the data every 5 seconds
      if (globals.interval_sec == now.second) {
        //add the next row in List
        row = [];
        //row.add(dataList[0]["Date"]);
        row.add(dataList[0]["Time"]);
        row.add(dataList[0]["Pulse"]);
        row.add(dataList[0]["SpO2"]);
        globals.associateLists!.add(row);

        globals.interval_sec =
            (globals.interval_sec + globals.interval) % 60;
      }
      //60 records in 5 minutes / 720 records in 60 minutes
      // if (globals.associateLists.length > 360) {
      //   //print("Save data List toCSV");
      //   await saveListToFile();
      // }
      // if (_playerState == PlayerState.ended){
      //   await saveListToFile();
      // }

    }
  }

  Future<void> saveListToFile() async {
    try {
      // Close BLE Connection
      // await widget.BLECon.disconnect();
      // Get the Downloads directory
      //String downloadsDirectory = (await getDownloadsDirectory())?.path ?? '';
      var len = globals.associateLists!.length;
      print("associateLists size: ${len}");
      String csv = const ListToCsvConverter().convert(globals.associateLists);
      print('DataInfo: ${csv}');
      String downloadsDirectory =
      await ExternalPath.getExternalStoragePublicDirectory(
          ExternalPath.DIRECTORY_DOWNLOADS);
      print(downloadsDirectory);
      //String path = "$downloadsDirectory/my_text_file.csv";
      //File file = await File(path).create(recursive: true);
      String fullname =
          "${downloadsDirectory}/log_${globals.HNID}_${globals.namedevice}_${globals.csv_file_name}.csv";
      print(fullname);
      // File file = File('${downloadsDirectory}/Pulse_SpO2_Log.csv');
      File file = File(fullname);
      await file.writeAsString(csv);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          //content: Text('File saved successfully at ${file.path}'),
          content: Text('หยุดและบันทึกข้อมูลสำเร็จ'),
        ),
      );
      //pop up
      //closeAppUsingSystemPop();
      // After saving, navigate back to the youtube_list screen
      // Navigator.pushReplacement(
      //   context,
      //   MaterialPageRoute(builder: (context) => goback.YoutubeExerciseList()),
      // );
      //or use
      Navigator.pop(context);
    } catch (e) {
      print('Error saving file: $e');
    }
  }

  void closeAppUsingExit() {
    SystemNavigator.pop();
    // exit(0);
  }

  @override
  Widget build(BuildContext context) {
    return YoutubePlayerBuilder(
      onExitFullScreen: () {
        SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
        setState(() {
          isFullScreen = false;
        });
      },
      onEnterFullScreen: () {
        SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
        setState(() {
          isFullScreen = true;
        });
      },
      player: YoutubePlayer(
        controller: _controller,
        showVideoProgressIndicator: true,
        bottomActions: [
          CurrentPosition(),
          ProgressBar(
            isExpanded: true,
            colors: const ProgressBarColors(
              playedColor: Colors.white70,
              handleColor: Colors.redAccent,
            ),
          ),
          RemainingDuration(),
          FullScreenButton(),
        ],
        aspectRatio: 16/8,
        onReady: () {
          _isPlayerReady = true;
        },
        onEnded: (data) async{
          _showSnackBar('สิ้นสุดการออกกำลังกาย!');
          if(globals.associateLists!.length > 2){
            await saveListToFile();
          }else{
            Navigator.pop(context,);
            // Navigator.pushReplacement(
            //   context,
            //   MaterialPageRoute(builder: (context) => goback.YoutubeExerciseList()),
            // );
          }
        },
      ),
      builder: (context, player) => Scaffold(
        resizeToAvoidBottomInset: true,
        appBar: AppBar(
          backgroundColor: Colors.greenAccent[100],
          centerTitle: true,
          leading: Image.asset('assets/images/BMEi.png'),
          title: const Text(
            //widget.videoTitle,
            "วิดีโอที่คุณเลือกชมขณะนี้",
            style: TextStyle(color: Colors.black, fontSize: 18),
            textAlign: TextAlign.center,
          ),
        ),
        body: ListView(
          children: [
            player,
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  _text('กิจกรรม', widget.videoCaption),
                  _space,
                  _text('ชื่อเรื่อง', widget.videoTitle),
                  _space,
                  _buildControls(),
                  // _space,
                  // _buildStateIndicator(),
                  _space,
                  _buildCircularSlider(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget get _space => const SizedBox(height: 10);

  Widget _text(String title, String value) {
    return RichText(
      text: TextSpan(
        text: '$title: ',
        style: const TextStyle(
          color: Colors.black,
          fontSize: 15,
          fontWeight: FontWeight.bold,
        ),
        children: [
          TextSpan(
            text: value,
            style: const TextStyle(
              color: Colors.black45,
              fontSize: 15,
              fontWeight: FontWeight.w300,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildControls() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        IconButton(
          icon: Icon(
            _controller.value.isPlaying ? Icons.pause : Icons.play_arrow,
          ),
          onPressed: _isPlayerReady
              ? () {
            _controller.value.isPlaying ? _controller.pause() : _controller.play();
            setState(() {
            });
          }
              : null,
        ),
        IconButton(
          icon: Icon(_muted ? Icons.volume_off : Icons.volume_up),
          onPressed: _isPlayerReady
              ? () {
            _muted ? _controller.unMute() : _controller.mute();
            setState(() {
              _muted = !_muted;
            });
          }
              : null,
        ),
        FullScreenButton(
          controller: _controller,
          color: Colors.black87,
        ),
        const Text(
          "Volume:",
          style: TextStyle(
            fontWeight: FontWeight.w300,
            color: Colors.black,
          ),
        ),
        Expanded(
          child: Slider(
            inactiveColor: Colors.transparent,
            value: _volume,
            min: 0.0,
            max: 100.0,
            divisions: 10,
            label: '${(_volume).round()}',
            onChanged: _isPlayerReady
                ? (value) {
              setState(() {
                _volume = value;
              });
              _controller.setVolume(_volume.round());
            }
                : null,
          ),
        ),
      ],
    );
  }

  Widget _buildStateIndicator() {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 800),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20.0),
        color: _getStateColor(_playerState),
      ),
      padding: const EdgeInsets.all(8.0),
      child: Text(
        _playerState.name,
        style: const TextStyle(
          fontWeight: FontWeight.w300,
          color: Colors.white,
        ),
        textAlign: TextAlign.center,
      ),
    );
  }

  Widget _buildCircularSlider(){
    return Container(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          SizedBox(
            height: 20,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Column(
                children: [
                  SleekCircularSliderWidget(pRbpm: globals.receivedDatafinger_PRbpm),
                  Text('Pulse'),
                ],
              ),
              // Padding(
              //   padding:
              //   EdgeInsets.fromLTRB(30, 50, 0, 0), // หรือใส่ค่าที่ต้องการ
              // ),
              // Column(
              //   children: [
              //     SleekCircularSliderWidget1(sp: globals.receivedDatafinger_SpO2),
              //     Text('SpO2'),
              //   ],
              // ),
            ], //children
          ),
          SizedBox(
            height: 20,
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                globals.DataReadStatus,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 14.0, // ปรับขนาดตัวหนังสือตามต้องการ
                  fontWeight: FontWeight.bold, // ตั้งค่าความหนาของตัวหนังสือ
                  color: Color.fromARGB(255, 4, 1, 8),
                ),
              ),
              SizedBox(
                height: 15,
              ),
              //_SaveExitButton(),
            ],
          ),
        ], // children
      ),
    );
  }

  Widget _SaveExitButton(){
    return ElevatedButton(
      style: ButtonStyle(
        backgroundColor: MaterialStateProperty.resolveWith<Color>(
              (Set<MaterialState> states) {
            if (states.contains(MaterialState.pressed)) {
              return Colors.redAccent;
            }
            return Colors.green;
          },
        ),
      ),
      onPressed: () => showDialog<String>(
        context: context,
        builder: (BuildContext context) => AlertDialog(
          title: const Text('กด "รับทราบ" คำชี้แจง'),
          content: const Text(
              'เมื่อบันทึกข้อมูลเสร็จ โปรแกรมจะปิดตัวเองอัตโนมัติ'),
          actions: <Widget>[
            ElevatedButton(
              onPressed: () async {
                await saveListToFile();
              },
              child: const Text('รับทราบ'),
            ),
          ],
        ),
      ),
      child: const Text('หยุดเพื่อบันทึกข้อมูล',
          style: TextStyle(
            fontSize: 18.0,
          )),
    );
  }

  Color _getStateColor(PlayerState state) {
    switch (state) {
      case PlayerState.unknown:
        return Colors.grey[700]!;
      case PlayerState.unStarted:
        return Colors.pink;
      case PlayerState.ended:
        return Colors.red;
      case PlayerState.playing:
        return Colors.lightGreen;
      case PlayerState.paused:
        return Colors.blue;
      case PlayerState.buffering:
        return Colors.yellow;
      case PlayerState.cued:
        return Colors.blue[900]!;
      default:
        return Colors.blue;
    }
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          message,
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontWeight: FontWeight.w300,
            fontSize: 16.0,
          ),
        ),
        backgroundColor: Colors.blueAccent,
        behavior: SnackBarBehavior.floating,
        elevation: 1.0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(50.0),
        ),
      ),
    );
  }
}
