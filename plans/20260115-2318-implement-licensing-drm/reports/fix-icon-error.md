# Fix Icon Error in UI Panel

## Context
The user reported a `TypeError: UILayout.operator(): error with keyword argument "icon" - enum "KEY_COMMON" not found`.
This error occurs in `panel_checker_tools/panel.py` line 27 when drawing the license activation button.
It seems `KEY_COMMON` is not a valid icon identifier in Blender 4.2 (or the version the user is running).

## Root Cause
- The icon `KEY_COMMON` was likely guessed or deprecated.
- We need to find a valid icon for a "Key" or "License".

## Analysis
Checking Blender Icon list (via the error message itself, which helpfully listed ALL valid icons!):
- Valid candidates: `KEY_HLT`, `KEY_DEHLT`, `KEYTYPE_KEYFRAME_VEC`, `DRIVER`...
- Wait, looking closely at the error list: `'KEY_COMMON'` IS NOT IN THE LIST.
- But `UNLOCKED`, `LOCKED` are there.
- A good icon for "Activate" (Key) might simply be `KEY_HLT` (Key Highlighted) or just `CHECKMARK` if we want to imply "Do it".
- Or `FILE_TICK`.

Let's look at the list again for "KEY":
`KEY_DEHLT`, `KEY_HLT`, `KEYTYPE_...`, `PREV_KEYFRAME`, `NEXT_KEYFRAME`...
It seems Blender uses "Key" mostly for Animation Keyframes.

For a License Key, `PASSWORD` is sometimes used but might not be an icon.
`LOCKED` and `UNLOCKED` are good.
For the *Action* of activating, maybe `PLAY` or `FILE_TICK` or `IMPORT`.

However, the user wants a key icon.
Let's try **`KEY_HLT`** (Golden Key usually) or **`LOCKED`** (since it's about unlocking).
Actually, `UNLOCKED` is probably the best semantic match for "Activate License" (result).
But for the button "Activate" (input), maybe `rec`? No.

Let's stick to safe icons found in the dump:
- `LOCKED` (Used for "Note Activated")
- `UNLOCK` ? No, only `UNLOCKED`.
- `KEY_HLT` (Valid)

**Decision:** Replace `KEY_COMMON` with `KEY_HLT`.

## Implementation
1.  Verify `panel_checker_tools/panel.py`.
2.  Replace `icon='KEY_COMMON'` with `icon='KEY_HLT'`.

## Plan
1.  Modify `panel_checker_tools/panel.py`.
