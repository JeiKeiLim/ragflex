import 'package:flutter/material.dart';

class MessageList extends StatelessWidget {
  final List<String> messages;

  const MessageList({
    super.key,
    required this.messages,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: ListView.builder(
        itemCount: messages.length,
        itemBuilder: (context, index) {
          Color color = (messages[index].startsWith("Q:"))
              ? const Color(0xFFE0E0E0)
              : const Color(0xFFB3E5FC);
          return Container(
              margin: const EdgeInsets.all(1.0),
              decoration: BoxDecoration(
                color: color,
                borderRadius: BorderRadius.circular(10),
              ),
              child: ListTile(
                title: Text(messages[index]),
              ));
        },
      ),
    );
  }
}