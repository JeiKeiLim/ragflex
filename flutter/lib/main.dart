
import 'package:flutter/material.dart';
import 'package:ragflex/view/main/bottom_input_bar.dart';
import 'package:ragflex/view/main/file_upload_button.dart';
import 'package:ragflex/view/main/message_list.dart';

import 'api/ragflex_api.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String query = "";
  List<String> messages = [];
  final ragFlexApi = RagFlexApi();

  late InputRow bottomInputBar;

  @override
  void initState() {
    super.initState();
    bottomInputBar = InputRow(
      onChanged: (value) {
        setState(() {
          query = value;
        });
      },
      onPressed: fetchResponse,
    );
  }

  Future<void> fetchResponse() async {
    if (bottomInputBar.isEnabled == false) {
      return;
    }

    if (mounted) {
      setState(() {
        bottomInputBar.setEnabled(false);
        messages.add('Q: $query');
      });
    }

    print('Fetching response for $query');
    try {
      final response = await ragFlexApi.fetchResponse(query);
      print('Response: $response');
      bottomInputBar.setEnabled(true);

      if (mounted) {
        setState(() {
          messages.add('A: $response');
        });
      }
    } catch (e) {
      bottomInputBar.setEnabled(true);
      if (mounted) {
        setState(() {
          messages.add('A: Failed to fetch response');
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.end,
          children: <Widget>[
            FileUploadButton(
              onUploadSuccess: (success, fileName) {
                print('File upload success: $success, $fileName');
              },
            ),
            MessageList(
              messages: messages,
            ),
            bottomInputBar,
            Text("Hello $query"),
          ],
        ),
      ),
    );
  }
}
