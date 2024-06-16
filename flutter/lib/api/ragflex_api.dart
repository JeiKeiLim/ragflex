import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

class RagFlexApi {
  static const String baseUrl = 'http://127.0.0.1:8000';

  Future<String> fetchResponse(String query) async {
    final url = ApiUrls.query.uri;
    final data = {
      "query": query,
      "context": {"k": 100, "distance_threshold": 0.5}
    };

    final response = await http.post(
      url,
      headers: ApiUrls.query.headers,
      body: json.encode(data),
    );

    if (response.statusCode == 200) {
      var decodedBody = utf8.decode(response.bodyBytes);

      return jsonDecode(decodedBody)['response'];
    } else {
      throw Exception('Failed to fetch response');
    }
  }

  Future<void> uploadFile(String fileName, Uint8List fileBytes) async {
    final url = ApiUrls.uploadFile.uri;
    final request = http.MultipartRequest('POST', url);
    request.files.add(http.MultipartFile.fromBytes('file', fileBytes, filename: fileName));
    final response = await request.send();

    if (response.statusCode != 200) {
      throw Exception('Failed to upload file');
    }
  }
}

enum ApiUrls {
  query,
  uploadFile,
}

extension ApiUrlExtension on ApiUrls {
  String get url {
    switch (this) {
      case ApiUrls.query:
        return '${RagFlexApi.baseUrl}/query';
      case ApiUrls.uploadFile:
        return '${RagFlexApi.baseUrl}/uploadfile';
    }
  }

  Uri get uri {
    return Uri.parse(url);
  }

  Map<String, String> get headers {
    switch (this) {
      case ApiUrls.query:
        return {'Content-Type': 'application/json'};
      case ApiUrls.uploadFile:
        return {};
    }
  }


}