

import 'package:flutter/material.dart';

class InputRow extends StatefulWidget {
  final Function(String) onChanged;
  final Function() onPressed;

  const InputRow({
    super.key,
    required this.onChanged,
    required this.onPressed,
  });

  @override
  _InputRowState createState() => _InputRowState();
}

class _InputRowState extends State<InputRow> {
  String query = "";

  @override
  Widget build(BuildContext context) {
    return Row(children: <Widget>[
      Expanded(
        flex: 1,
        child: TextField(
          key: const ValueKey('nameField'),
          onChanged: (value) {
            setState(() {
              query = value;
            });
            widget.onChanged(query);
          },
          decoration: const InputDecoration(
            hintText: 'What\'s on your mind?',
          ),
        ),
      ),
      const SizedBox(width: 10),
      ElevatedButton(
        onPressed: () {
          if (mounted) {
            setState(() {
              query = "";
            });
          }
          widget.onPressed();
        },
        child: const Text('Submit'),
      ),
    ]);
  }
}