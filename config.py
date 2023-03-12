import os
import copy
import subprocess
from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

laptop = False
if "DEVICE" in os.environ:
    if os.environ['DEVICE'] == "laptop":
        bar_col="#000000.0"
        laptop = True
else:
    bar_col="#000000.0"

x = 3

# qtile-gnome
@hook.subscribe.startup
def dbus_register():
    id = os.environ.get("DESKTOP_AUTOSTART_ID")
    if not id:
        return
    subprocess.Popen(
        [
            "dbus-send",
            "--session",
            "--print-reply",
            "--dest=org.gnome.SessionManager",
            "/org/gnome/SessionManager",
            "org.gnome.SessionManager.RegisterClient",
            "string:qtile",
            "string:" + id,
        ]
    )


"""
To Do list
    - separate config into different files
    - eww widgets and bars
    - add background blur
    - Add Better floating window support
    - full nord theme with theme file in main config
    - handle floating windows so they are still in the stack
    - prevent window switching when moving to current window
    - status bar same as background
    - Change application launcher
    - Change system icons
    - change login window background

"""

"""
** Code to add to layout class in libqtile/layout/base.py
    def cmd_increase_margin(self):
        self.margin += 5
        self.group.layout_all()

    def cmd_decrease_margin(self):
        new_margin = self.margin - 5
        if new_margin < 0:
            new_margin = 0

        self.margin = new_margin

        self.group.layout_all()

"""

mod = "mod4"
terminal = guess_terminal()


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call([home])


@lazy.function
def inc_margins(qtile):
    qtile.current_layout.margin += 5
    qtile.current_group.layout_all()


@lazy.function
def dec_margins(qtile):
    qtile.current_layout.margin -= 5
    qtile.current_group.layout_all()

@lazy.function
def workmanp(qtile):
    # Change the keyboardlayout widget text
    qtile.cmd_spawn(os.path.expanduser("~/.config/qtile/workmanp.sh"))

@lazy.function
def change_time_format(qtile):
    if qtile.widgets_map["clock"].format == "%a %d/%m/%Y %H:%M":
        qtile.widgets_map["clock"].format = "%a %d/%m/%Y %H:%M:%S"
    else:
        qtile.widgets_map["clock"].format = "%a %d/%m/%Y %H:%M"


keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panange s
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "control"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.spawn('rofi -show drun'), desc="Run rofi"),
    # Change the volume if our keyboard has keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 -q set Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 -q set Master 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -c 0 -q set Master toggle")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    Key([mod], "Up", inc_margins, desc="Increase layout margins"),
    Key([mod], "Down", dec_margins, desc="Decrease layout margins"),
    ### Switch focus to specific monitor (out of three)
    Key(
        [mod, "shift"], "period", lazy.to_screen(1), desc="Keyboard focus to monitor 1"
    ),
    Key([mod, "shift"], "comma", lazy.to_screen(0), desc="Keyboard focus to monitor 2"),
    ### Switch focus of monitors
    Key([mod], "period", lazy.to_screen(1), desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.to_screen(0), desc="Move focus to prev monitor"),
#    Key([mod, "shift"], "1", lazy.spawn("setxkbmap -layout gb -option -option 'caps:swapescape'")),
#    Key([mod, "shift"], "2", lazy.spawn("setxkbmap -layout se -option -option 'caps:swapescape'")),
#    Key([mod, "shift"], "3", lazy.spawn("setxkbmap -layout no -option -option 'caps:swapescape'")),
#    Key([mod, "shift"], "4", lazy.spawn("setxkbmap -layout cn -option -option 'caps:swapescape'")),
#    Key([mod, "shift"], "5", lazy.spawn("setxkbmap -layout us -option -variant dvp -option compose:102 -option numpad:shift3 -option kpdl:semi -option keypad:atm -option 'caps:swapescape'")),
#    Key([mod, "shift"], "6", change_time_format, desc="Change the time format"),
#    Key([mod, "shift"], "7", lazy.spawn("setxkbmap -layout us -variant workman -option 'caps:swapescape'")),
#    Key([mod, "shift"], "8", lazy.spawn("setxkbmap -layout us -option 'caps:swapescape'")),
    # Alternatives when workmanp being used
#    Key([mod], "exclam", lazy.spawr("setxkbmap -layout gb -option 'caps:swapescape'")),
#    Key([mod], "at", lazy.spawn("setxkbmap -layout se -option 'caps:swapescape'")),
#    Key([mod], "numbersign", lazy.spawn("setxkbmap -layout no -option 'caps:swapescape'")),
#    Key([mod], "dollar", lazy.spawn("setxkbmap -layout cn -option 'caps:swapescape'")),
#    Key([mod], "percent", lazy.spawn("setxkbmap -layout ru -option 'caps:swapescape'")),
#    Key([mod], "asciicircum", change_time_format, desc="Change the time format"),
#    Key([mod], "ampersand", lazy.spawn("setxkbmap -layout us -variant workman -option 'caps:swapescape'")),
#    Key([mod], "8", lazy.spawn("setxkbmap -layout us -option 'caps:swapescape'"), workmanp, desc="Change to workmanp layout"),
    #Key([mod], "Right", lazy.spawn("sh ~/.config/qtile/spotify_control -option 'next'"), desc="Change media in spotify"),
    Key([mod], "Right", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player"), desc="Change media in spotify"),

    Key([mod], "x", lazy.window.toggle_fullscreen()),

]

groups = [Group(i) for i in "123456789"]
# alt_dvk = [i for i in "+[{(/\)}]"]

alt_names = ["plus", "bracketleft", "braceleft", "parenleft", "slash", "backslash", "parenright", "braceright", "bracketright"]

for index, i in enumerate(groups):
    keys.extend(
        [
            Key(
                [mod],
                alt_names[index],
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                alt_names[index],
                lazy.window.togroup(i.name),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "term",
                "alacritty",
                x=0.0,
                y=0.0,
                width=(1.0 / 5.0),
                height=1.0,
                opacity=0.8,
                on_focus_lost_hide=True,
            )
        ],
    )
)

keys.extend([Key([mod], "n", lazy.group["scratchpad"].dropdown_toggle("term"))])

layout_theme = {"border_focus": "ffffff", "border_normal": "000000", "border_width": 2, "border_focus_stack":"ff0000","border_normal_stack":"ff0000"}

# margin_value = 15
layouts = [
    layout.Columns(
        margin=15,
        margin_on_single=25,
        wrap_focus_columns=False,
        wrap_focus_rows=False,
        wrap_focus_stacks=False,
        **layout_theme
        # margin= margin_value,
        # margin_on_single = margin_value*1.5
    ),
    layout.Max(**layout_theme),
    layout.TreeTab(**layout_theme),
    layout.Floating(**layout_theme),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
if laptop:
    widgets = [[widget.GroupBox(),
            widget.Prompt(),
            widget.Spacer(length=bar.STRETCH),
            widget.Systray(),
            #widget.WidgetBox(widgets=[
            #    widget.TextBox(text="This is a test"),
            #    widget.WindowName()
            #], close_button_location="right"),
            widget.BatteryIcon(),
            widget.Battery(
                energy_now_file="charge_now",
                energy_full_file="charge_full",
                power_now_file="current_now",
                update_delay=5,
                foreground="7070ff",
                format="{percent:2.0%}"
            ),
                widget.KeyboardLayout(configured_keyboards=['gb', 'se', 'no', 'cn', 'ru', 'us'], display_map={"us workman":"WK", "us":"WKP"}),
            widget.PulseVolume(),
                widget.Clock(format="%a %d/%m/%Y %H:%M:%S", mouse_callbacks={"Button1":change_time_format}),
            widget.Wallpaper(
                directory="~/.config/qtile/wallpaper/",
                wallpaper_command=["feh", "--bg-fill"],
                label="",
            )
            ] for i in range(2)]
else:
    widgets = [[widget.GroupBox(),
            widget.Prompt(),
            widget.Spacer(length=bar.STRETCH),
            widget.Systray(),
                widget.KeyboardLayout(configured_keyboards=['gb', 'se', 'no', 'cn', 'ru'], display_map={"us workman":"WK"}),
            widget.PulseVolume(),
            widget.Clock(format="%a %d/%m/%Y %H:%M:%S", mouse_callbacks={"Button1":change_time_format}),
            widget.Wallpaper(
                directory="~/.config/qtile/wallpaper/",
                wallpaper_command=["feh", "--bg-fill"],
                label="",
            )
            ] for i in range(2)]

screens = [
    Screen(
        top=bar.Bar(
            widgets[0],
            30,
            background="#000000.0",
            opacity=1,
        ),
    ),
    Screen(
        top=bar.Bar(
            widgets[1],
            30,
            background="#000000.0",
            opacity=1,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
cursor_warp = False
# floating_layout = layout.Floating(
#    float_rules=[
#        # Run the utility of `xprop` to see the wm class and name of an X client.
#        layout.Floating.default_float_rules,
#        Match(wm_class="confirmreset"),  # gitk
#        Match(wm_class="makebranch"),  # gitk
#        Match(wm_class="maketag"),  # gitk
#        Match(wm_class="ssh-askpass"),  # ssh-askpass
#        Match(title="branchdialog"),  # gitk
#        Match(title="pinentry"),  # GPG key password entry
#    ]
# )
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
bring_front_click = False

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# Automatically float these types. This overrides the default behavior (which
# is to also float utility types), but the default behavior breaks our fancy
# gimp slice layout specified later on.
floating_layout = layout.Floating(
    auto_float_types=[
        "notification",
        "toolbar",
        "splash",
        "dialog",
    ]
)

# handling screens
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


reconfigure_screens = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
