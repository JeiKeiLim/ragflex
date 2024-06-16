import 'package:flutter/material.dart';

class MessageList extends StatefulWidget {
  final List<String> messages;

  const MessageList({
    super.key,
    required this.messages,
  });

  void clearMessages() {
    messages.clear();
  }

  @override
  _MessageListState createState() => _MessageListState();
}

class _MessageListState extends State<MessageList> {
  final ScrollController _controller = ScrollController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _controller.jumpTo(_controller.position.maxScrollExtent);
    });
  }

  @override
  void didUpdateWidget(MessageList oldWidget) {
    super.didUpdateWidget(oldWidget);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _controller.animateTo(_controller.position.maxScrollExtent,
          duration: const Duration(milliseconds: 200), curve: Curves.easeOut);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: ListView.builder(
        controller: _controller,
        itemCount: widget.messages.length,
        itemBuilder: (context, index) {
          Color color = (widget.messages[index].startsWith("Q:"))
              ? const Color(0xFFE0E0E0)
              : const Color(0xFFB3E5FC);
          return Container(
              margin: const EdgeInsets.all(1.0),
              decoration: BoxDecoration(
                color: color,
                borderRadius: BorderRadius.circular(10),
              ),
              child: ListTile(
                title: Text(widget.messages[index]),
              ));
        },
      ),
    );
  }
}
