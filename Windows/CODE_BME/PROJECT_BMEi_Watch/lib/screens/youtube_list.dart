import 'package:flutter/material.dart';
import 'package:youtube_metadata/youtube_metadata.dart';
import 'package:transparent_image/transparent_image.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'setting.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'youtube_play.dart';
import '../utils/BLEConnect.dart';
import '../utils/snackbar.dart';

class YoutubeVideo {
  final String title;
  final String TH_title;
  final List<String> links;
  final List<String> events;
  List<MetaDataModel?> videoDataList;

  YoutubeVideo({required this.title, required this.TH_title, required this.links, required this.events})
      : videoDataList = List.filled(links.length, null);
}

final List<YoutubeVideo> youtubeVideos = [
  YoutubeVideo(title: 'Basic', TH_title: 'ระดับเบา',
      links: [
    'https://www.youtube.com/watch?v=8BcPHWGQO44',
    'https://www.youtube.com/watch?v=Ev6yE55kYGw',
    'https://www.youtube.com/watch?v=oumzMyqK-2I',],
      events: ['การออกกำลังกายระดับเบา แบบที่ 1', 'การออกกำลังกายระดับเบา แบบที่ 2','การออกกำลังกายระดับเบา แบบที่ 3',]),
  YoutubeVideo(title: 'Intermediate', TH_title: 'ระดับปานกลาง',
      links: [
    'https://www.youtube.com/watch?v=8NemLjfqy24',
    'https://www.youtube.com/watch?v=E2YqFYFLSbE',],
      events: ['การออกกำลังกายระดับปานกลาง แบบที ่1', 'การออกกำลังกายระดับปานกลาง แบบที่ 2',]),
  YoutubeVideo(title: 'Advance', TH_title: 'ระดับหนัก',
      links: [
    'https://www.youtube.com/watch?v=bO6NNfX_1ns',],
      events: ['การออกกำลังกายระดับหนัก แบบที่ 1']),
];

class YoutubeList extends StatefulWidget {
  const YoutubeList({super.key});

  @override
  _YoutubeListState createState() => _YoutubeListState();
}

class _YoutubeListState extends State<YoutubeList> {
  @override
  late String savedText1;
  late String savedText2;

  late BLEConnect myBLE = BLEConnect();

  void initState() {
    super.initState();
    loadConfig();
    fetchVideoData(); // Call fetchData() to load the data
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

  Future<void> fetchVideoData() async {
    await Future.wait(youtubeVideos.map((category) async {
      category.videoDataList = await fetchAllMetadata(category.links);
    }));
    setState(() {}); // Refresh the UI after data is fetched
  }

  Future<List<MetaDataModel?>> fetchAllMetadata(List<String> youtubeLinks) async {
    List<MetaDataModel?> metadata = List.filled(youtubeLinks.length, null);
    for (int i = 0; i < youtubeLinks.length; i++) {
      final link = youtubeLinks[i];
      final Uri uri = Uri.parse("https://www.youtube.com/oembed?url=$link&format=json");

      try {
        final result = await http.get(uri);
        final resultJson = json.decode(result.body);
        metadata[i] = MetaDataModel.fromMap(resultJson);
      } catch (e) {
        print("Error fetching metadata for $link: $e");
      }
    }
    return metadata;
  }

  Future<void> refreshPage() async {
    await fetchVideoData();  // Re-fetch video data
    myBLE.startBluetoothConnectionfinger(context);  // Restart Bluetooth connection
  }

  void refreshPage1() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("ค้นหาอุปกรณ์ รอสักครู่..."),backgroundColor: Colors.green),
    );
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const YoutubeList()),
    );
  }


  @override
  Widget build(BuildContext context) {
    final ColorScheme colorScheme = Theme.of(context).colorScheme;
    final Color oddItemColor = colorScheme.primary.withOpacity(0.05);
    final Color evenItemColor = colorScheme.primary.withOpacity(0.15);
    return DefaultTabController(
      initialIndex: 0,
      length: youtubeVideos.length,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('ชุดออกกำลังกาย',style: TextStyle(fontSize: 18)),
            backgroundColor: Colors.greenAccent[100],
            leading: Image.asset('assets/images/BMEi.png'),
            actions: <Widget>[
              IconButton(
                icon: const Icon(
                  Icons.search_outlined,
                  color: Colors.white,
                ),
                onPressed: refreshPage1,
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
          // notificationPredicate: (ScrollNotification notification) {
          //   return notification.depth == 1;
          // },
          // The elevation value of the app bar when scroll view has
          // scrolled underneath the app bar.
          scrolledUnderElevation: 4.0,
          shadowColor: Theme.of(context).shadowColor,
          bottom: TabBar(
            tabs: youtubeVideos.map((video) {
              return Tab(
                icon: Image.asset('assets/images/SF_${video.title.toLowerCase()}.png', width: 35, height: 35,),
                text: video.TH_title,
              );
            }).toList(),
          ),
        ),
        body: RefreshIndicator(
            onRefresh: refreshPage,
            child: Stack(
              children: [
                Positioned.fill(
                  child:
                  Image.asset("assets/images/AMS_BMEI.png",
                    fit: BoxFit.contain,
                  ),
                ),
                TabBarView(
                      children: youtubeVideos.map((video) {
                        return youtubePlayList(links: video.links, captions: video.events, videoDataList: video.videoDataList, BLECon: myBLE);
                      }).toList(),
                    ),
              ],
            ),
        ),
        // body: RefreshIndicator(
        //   onRefresh: refreshPage,
        //   child: TabBarView(
        //     children: youtubeVideos.map((video) {
        //       return youtubePlayList(link: video.links, captions: video.events, videoDataList: video.videoDataList, BLECon: myBLE);
        //     }).toList(),
        //   ),
        // ),
      ),
    );
  }
}

Widget youtubePlayList({required List<String> links, required List<String> captions, required List<MetaDataModel?> videoDataList, required BLEConnect BLECon}) {
  if (videoDataList.isEmpty || videoDataList.every((element) => element == null)) {
    return const Center(child: CircularProgressIndicator());
  }

  return ListView.builder(
    shrinkWrap: true,
    physics: const ScrollPhysics(),
    itemCount: links.length,
    itemBuilder: (context, index) {
      final linkURL = links[index];
      final thumbnail = getYoutubeThumbnail(links[index]);
      final metaData = videoDataList[index];
      final eventTitle = captions[index];

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
                ClipRRect(
                  borderRadius: const BorderRadius.only(
                    topLeft: Radius.circular(8.0),
                    topRight: Radius.circular(8.0),
                  ),
                  child: FadeInImage.memoryNetwork(
                    placeholder: kTransparentImage,
                    image: thumbnail ?? '',
                    fit: BoxFit.scaleDown,
                    alignment: Alignment.center,
                    filterQuality: FilterQuality.high,
                  ),
                ),
                GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => VideoPlay(
                          videoURL: linkURL,
                          videoTitle: metaData != null ? metaData.title! : 'ไม่มีชื่อ',
                          videoCaption: eventTitle,
                          // BLECon: BLECon,
                        ),
                      ),
                    );
                  },
                  child: const CircleAvatar(
                    radius: 30,
                    backgroundColor: Colors.black45,
                    child: Icon(
                      Icons.play_arrow,
                      size: 40,
                      color: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
            ListTile(
              title: Text(
                metaData != null ? metaData.title! : 'กำลังโหลด...',
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
      );
    },
  );
}

String? getYoutubeThumbnail(String videoUrl) {
  final uri = Uri.parse(videoUrl);
  if (uri.host == "youtu.be") {
    return 'https://img.youtube.com/vi/${uri.pathSegments.first}/0.jpg';
  } else {
    return 'https://img.youtube.com/vi/${uri.queryParameters['v']}/0.jpg';
  }
}
