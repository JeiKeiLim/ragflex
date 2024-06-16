import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:ragflex/api/ragflex_api.dart';

typedef UploadCallback = void Function(bool success, String fileName);

class FileUploadButton extends StatefulWidget {
  final UploadCallback onUploadSuccess;

  const FileUploadButton({super.key, required this.onUploadSuccess});

  @override
  FileUploadButtonState createState() => FileUploadButtonState(onUploadSuccess: onUploadSuccess);
}

class FileUploadButtonState extends State<FileUploadButton> {
  Uint8List? _fileBytes;
  String? _fileName;
  String? _filePath;
  String _fileNameText = '';

  final UploadCallback onUploadSuccess;

  FileUploadButtonState({required this.onUploadSuccess});

  Uint8List? get fileBytes => _fileBytes;

  String? get fileName => _fileName;

  Future pickFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();

    if (result != null) {
      _fileBytes = result.files.single.bytes;
      _fileName = result.files.single.name;
      _filePath = result.files.single.path;

      uploadFile();
    } else {
      onUploadSuccess(false, '#NO_FILE_SELECTED#');
    }
  }

  Future uploadFile() async {
    if ((_fileBytes == null && _filePath == null) || _fileName == null) {
      onUploadSuccess(false, fileName == null ? '' : fileName!);
      return;
    }

    var request = http.MultipartRequest('POST', Uri.parse(ApiUrls.uploadFile.url));
    if (_fileBytes != null) {
      request.files.add(await http.MultipartFile.fromBytes(
          'file', _fileBytes!, filename: _fileName!));
    }
    else if (_filePath != null) {
      request.files.add(await http.MultipartFile.fromPath(
          'file', _filePath!));
    }
    var res = await request.send();

    if (res.statusCode == 200) {

      if (mounted) {
        setState(() {
          _fileNameText = 'File uploaded: $_fileName';
        });
      }

      onUploadSuccess(true, fileName!);
    } else {
      onUploadSuccess(false, fileName!);

    }
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        ElevatedButton(
          onPressed: pickFile,
          child: Text('Upload file'),
        ),
        const SizedBox(width: 10),
        Text(_fileNameText)
      ],
    );
  }
}
