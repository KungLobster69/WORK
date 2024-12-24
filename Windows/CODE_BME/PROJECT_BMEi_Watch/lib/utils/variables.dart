int receivedDatafinger_PRbpm = 0;
int receivedDatafinger_SpO2 = 0;
String DataReadStatus = '';

String HNID = "";
String macaddress = "";
String namedevice ="";
String exIndex = "0";
bool header_added = false;
List<List<dynamic>>? associateLists = [];
int interval_sec = 0;
int interval = 5;
String csv_file_name = "";

// List of allowed values for the dropdown
final List<String> dropdownItems = ['ระดับพื้นฐาน', 'ระดับกลาง', 'ระดับสูง'];