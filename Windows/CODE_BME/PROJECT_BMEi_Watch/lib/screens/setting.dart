import 'dart:developer';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'youtube_list.dart' as goback;

class HomePagesetting extends StatefulWidget {
  @override
  HomePageStatesetting createState() => HomePageStatesetting();

}

class HomePageStatesetting extends State<HomePagesetting> {
  final TextEditingController _textController1 = TextEditingController();
  final TextEditingController _textController2 = TextEditingController();

  final String _storageKey1 = 'user_input_key1';
  final String _storageKey2 = 'user_input_key2';


  @override
  void initState() {
    super.initState();
    loadSavedText();
  }

  Future<void> loadSavedText() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String savedText1 = prefs.getString(_storageKey1) ?? '';
    String savedText2 = prefs.getString(_storageKey2) ?? '';
    setState(() {
      _textController1.text = savedText1;
      _textController2.text = savedText2;
    });
  }

  Future<void> _saveText() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString(_storageKey1, _textController1.text);
    await prefs.setString(_storageKey2, _textController2.text);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        //content: Text('File saved successfully at ${file.path}'),
        content: Text('บันทึกข้อมูลสำเร็จ'),
      ),
    );
    if(_textController1.text.isNotEmpty && _textController1.text.isNotEmpty) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const goback.YoutubeList()),
      );
    }
  }

  Future<void> _saveWarning() async {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        //content: Text('File saved successfully at ${file.path}'),
        content: Text('กรุณากรอกข้อมูลให้ครบ'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('การตั้งค่าผู้ใช้งาน'),

        // leading: Image.asset('assets/images/SF.png'),
          actions: <Widget>[
            Image.asset('assets/images/BMEi.png')
          ],

        backgroundColor: Colors.greenAccent[100],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          //mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            TextField(
              controller: _textController1,
              decoration: const InputDecoration(
                labelText: 'ชื่อผู้ใช้งาน (ภาษาอังกฤษ)',
                labelStyle: TextStyle(fontSize: 18),
              ),
              // onChanged: (value) {
              //   _saveText();
              // },
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _textController2,
              decoration: const InputDecoration(
                labelText: 'หมายเลขอุปกรณ์ (ดูที่นาฬิกา)',
                labelStyle: TextStyle(fontSize: 18),
              ),
              // onChanged: (value) {
              //   _saveText();
              // },
              keyboardType: TextInputType.number,
            ),
            const SizedBox(height: 10),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                String userInput1 = _textController1.text;
                String userInput2 = _textController2.text;
                if(userInput1.isNotEmpty && userInput2.isNotEmpty) {
                  _saveText();
                }else{
                  _saveWarning();
                }
              },
              child: const Text('จำข้อมูลผู้ใช้งาน'),
            ),
            ElevatedButton(
              onPressed: () {
                _textController1.clear();
                _textController2.clear();
                _saveText();
                print('Text cleared');
              },
              style: ButtonStyle(
                backgroundColor: MaterialStateProperty.all<Color>(
                    const Color.fromARGB(255, 189, 64, 26)), // กำหนดสีเมื่อปกติ
                // สามารถกำหนดสีในสถานะต่าง ๆ ได้เช่นเมื่อกด
                //overlayColor: MaterialStateProperty.all<Color>(Colors.red),
              ),
              child: const Text('ล้างข้อมูลผู้ใช้งาน'),
            ),
          ],
        ),
      ),
    );
  }
}

class CustomTextInputFormatter extends TextInputFormatter{
  final String sample;
  final String separator;

  CustomTextInputFormatter({
    required this.sample,
    required this.separator,
  }){
    assert(sample != null);
    assert(separator != null);
  }

  @override
  TextEditingValue formatEditUpdate(TextEditingValue oldValue, TextEditingValue newValue){

    if(newValue.text.length > 0) {
      log('Now: length ${newValue.text.length}');
      if(newValue.text.length > oldValue.text.length){
        if(newValue.text.length > sample.length) return oldValue;
        if(newValue.text.length < sample.length && sample[newValue.text.length - 1] == separator){
          return TextEditingValue(
            text: '${oldValue.text}$separator${newValue.text.substring(newValue.text.length - 1)}',
            selection: TextSelection.collapsed(offset: newValue.selection.end+1),
          );
        }
      }
    }
    return newValue;
  }

}