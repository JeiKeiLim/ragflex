import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class InputRow extends StatefulWidget {
  final Function(String) onChanged;
  final Function() onPressed;

  final GlobalKey<InputRowState> stateKey;

  factory InputRow({
    required Function(String) onChanged,
    required Function() onPressed,
  }) {
    final stateKey = GlobalKey<InputRowState>();
    return InputRow._(
        onChanged: onChanged, onPressed: onPressed, stateKey: stateKey);
  }

  const InputRow._({
    required this.onChanged,
    required this.onPressed,
    required this.stateKey,
  }) : super(key: stateKey);

  @override
  InputRowState createState() => InputRowState();

  void setEnabled(bool enabled) {
    stateKey.currentState?.setEnabled(enabled);
  }

  bool get isEnabled => stateKey.currentState?._isEnabled ?? false;
}

class InputRowState extends State<InputRow> {
  String query = "";
  final TextEditingController _controller = TextEditingController();

  final FocusNode _focusNode = FocusNode();
  final FocusNode _textFieldFocusNode = FocusNode();

  bool _isShiftPressed = false;
  bool _isEnabled = true;

  String hintText = 'What\'s on your mind?';

  void setEnabled(bool enabled) {
    if (mounted) {
      setState(() {
        _isEnabled = enabled;

        if (_isEnabled) {
          hintText = 'What\'s on your mind?';
          WidgetsBinding.instance.addPostFrameCallback((_) {
            _textFieldFocusNode.requestFocus();
          });
        } else {
          hintText = 'Please wait...';
        }
      });
    }
  }

  void clearTextField() {
    setState(() {
      query = "";
    });
    _controller.clear();
    _textFieldFocusNode.requestFocus();
  }

  void submitQuery() {
    if (query.trim().isEmpty) {
      clearTextField();
      return;
    }
    widget.onPressed();
    widget.onChanged(query);
    clearTextField();
  }

  @override
  Widget build(BuildContext context) {
    return Row(children: <Widget>[
      Expanded(
        flex: 1,
        child: KeyboardListener(
          focusNode: _focusNode,
          onKeyEvent: (event) {
            if (event is KeyDownEvent) {
              if (event.logicalKey == LogicalKeyboardKey.shiftLeft ||
                  event.logicalKey == LogicalKeyboardKey.shiftRight) {
                _isShiftPressed = true;
              }

              if (!_isShiftPressed &&
                  event.logicalKey == LogicalKeyboardKey.enter) {
                submitQuery();
              }
            }

            // Detect key up
            if (event is KeyUpEvent) {
              if (event.logicalKey == LogicalKeyboardKey.shiftLeft ||
                  event.logicalKey == LogicalKeyboardKey.shiftRight) {
                _isShiftPressed = false;
              }
            }
          },
          child: TextField(
            key: const ValueKey('nameField'),
            controller: _controller,
            focusNode: _textFieldFocusNode,
            keyboardType: TextInputType.multiline,
            maxLines: null,
            onChanged: (value) {
              if (value.trim().isEmpty) {
                clearTextField();
                return;
              }
              setState(() {
                query = value;
              });
              widget.onChanged(query);
            },
            decoration: InputDecoration(
              hintText: hintText,
            ),
            enabled: _isEnabled,
          ),
        ),
      ),
      const SizedBox(width: 10),
      ElevatedButton(
          onPressed: _isEnabled
              ? () {
                  submitQuery();
                }
              : null,
          child: const Text('Submit'),
          style: ButtonStyle(
            backgroundColor: MaterialStateProperty.resolveWith<Color>(
              (Set<MaterialState> states) {
                if (states.contains(MaterialState.disabled)) {
                  return Colors
                      .grey; // Use the color you want for disabled state
                }
                return Theme.of(context)
                        .elevatedButtonTheme
                        .style
                        ?.backgroundColor
                        ?.resolve(states) ??
                    Theme.of(context).colorScheme.primary;
              },
            ),
            foregroundColor: MaterialStateProperty.resolveWith<Color>(
              (Set<MaterialState> states) {
                if (states.contains(MaterialState.disabled)) {
                  return Colors
                      .white; // Use the color you want for disabled state
                }
                return Theme.of(context)
                        .elevatedButtonTheme
                        .style
                        ?.foregroundColor
                        ?.resolve(states) ??
                    Theme.of(context).colorScheme.onPrimary;
              },
            ),
          ),
      ),
    ]);
  }

  @override
  void dispose() {
    _controller.dispose();
    _focusNode.dispose();
    _textFieldFocusNode.dispose();
    super.dispose();
  }
}
