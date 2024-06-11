import 'dart:convert';

import 'package:http/http.dart' as http;

class PDFRagApi {
  static const String baseUrl = 'http://127.0.0.1:8000';

  Future<String> fetchResponse(String query) async {
    final url = Uri.parse('$baseUrl/query');
    final data = {
      "query": query,
      "context": {"k": 100, "distance_threshold": 0.5}
    };

    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: json.encode(data),
    );

    if (response.statusCode == 200) {
      var decodedBody = utf8.decode(response.bodyBytes);

      return jsonDecode(decodedBody)['response'];
    } else {
      throw Exception('Failed to fetch response');
    }
  }
}
