import 'package:flutter/material.dart';
import 'package:youtube_metadata/youtube_metadata.dart';
import 'package:transparent_image/transparent_image.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'youtube_display.dart';

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
        'https://www.youtube.com/watch?v=7w286B6eUN4',],
      events: ['การออกกำลังกายใช้แรงต้าน ระดับเบา',]),
  YoutubeVideo(title: 'Intermediate', TH_title: 'ระดับปานกลาง',
      links: [
        'https://www.youtube.com/watch?v=EpRLaQv_ztM',],
      events: ['การออกกำลังกายใช้แรงต้าน ระดับปานกลาง',]),
  YoutubeVideo(title: 'Advance', TH_title: 'ระดับหนัก',
      links: [
        'https://www.youtube.com/watch?v=HuUzRbGbzI0',],
      events: ['การออกกำลังกายใช้แรงต้าน ระดับหนัก']),
];

class YoutubeControlList3 extends StatefulWidget {
  const YoutubeControlList3({super.key});

  @override
  _YoutubeControlListState createState() => _YoutubeControlListState();
}

class _YoutubeControlListState extends State<YoutubeControlList3> {
  @override
  void initState() {
    super.initState();
    fetchVideoData(); // Call fetchData() to load the data
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
    // myBLE.startBluetoothConnectionfinger(context);  // Restart Bluetooth connection
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
                  return youtubePlayList(link: video.links, captions: video.events, videoDataList: video.videoDataList);
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

Widget youtubePlayList({required List<String> link, required List<String> captions, required List<MetaDataModel?> videoDataList}) {
  if (videoDataList.isEmpty || videoDataList.every((element) => element == null)) {
    return const Center(child: CircularProgressIndicator());
  }

  return ListView.builder(
    shrinkWrap: true,
    physics: const ScrollPhysics(),
    itemCount: link.length,
    itemBuilder: (context, index) {
      final linkURL = link[index];
      final thumbnail = getYoutubeThumbnail(link[index]);
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
                        builder: (context) => VideoPlayHR(
                          videoURL: linkURL,
                          videoTitle: metaData != null ? metaData.title! : 'ไม่มีชื่อ',
                          videoCaption: eventTitle,
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
