const std = @import("std");

const BASE = "E:\\AI_Tools\\ai-tool-curator";
const SERVER_CMD = BASE ++ "\\start-server.cmd";
const RUN_CMD = BASE ++ "\\run.cmd";
const VAULT_DIR = BASE ++ "\\vault";
const DATA_DIR = BASE ++ "\\data\\raw";
const CONFIG_FILE = BASE ++ "\\config.yaml";

const W = 580;
const H = 600;
const BTN_W = 130;
const BTN_H = 32;
const GRP_X = 12;
const GRP_W = W - 24;

const ID_START = 1001;
const ID_STOP = 1002;
const ID_RUN = 1003;
const ID_VAULT = 1004;
const ID_DATA = 1005;
const ID_CFG = 1006;
const ID_CLRLOG = 1007;
const ID_TMR = 2001;

const BOOL = i32;
const DWORD = u32;
const UINT = u32;
const LONG = i32;
const WORD = u16;
const WPARAM = u64;
const LPARAM = i64;
const LRESULT = i64;
const LPVOID = *anyopaque;
const LPCSTR = [*:0]const u8;
const LPSTR = [*:0]u8;
const HINSTANCE = *anyopaque;
const HWND = *anyopaque;
const HICON = *anyopaque;
const HCURSOR = *anyopaque;
const HBRUSH = *anyopaque;
const HANDLE = *anyopaque;

const TRUE = 1;
const FALSE = 0;
const NULL = @as(*anyopaque, @ptrFromInt(0));

const WS_CHILD: DWORD = 0x40000000;
const WS_VISIBLE: DWORD = 0x10000000;
const WS_VSCROLL: DWORD = 0x00200000;
const WS_OVERLAPPEDWINDOW: DWORD = 0x00CF0000;
const SS_LEFT: DWORD = 0x00000000;
const SS_ETCHEDHORZ: DWORD = 0x00000010;
const BS_PUSHBUTTON: DWORD = 0x00000000;
const ES_MULTILINE: DWORD = 0x00000004;
const ES_READONLY: DWORD = 0x00000800;
const ES_AUTOVSCROLL: DWORD = 0x00000040;
const CS_HREDRAW: UINT = 0x0002;
const CS_VREDRAW: UINT = 0x0001;
const SW_SHOWNORMAL: i32 = 1;
const SW_HIDE: i32 = 0;
const SWP_NOMOVE: UINT = 0x0002;
const SWP_NOZORDER: UINT = 0x0004;
const CW_USEDEFAULT: i32 = -2147483648;
const WM_CREATE: UINT = 0x0001;
const WM_CLOSE: UINT = 0x0010;
const WM_DESTROY: UINT = 0x0002;
const WM_COMMAND: UINT = 0x0111;
const WM_TIMER: UINT = 0x0113;
const WM_SIZE: UINT = 0x0005;
const EM_GETLIMITTEXT: UINT = 0x00D5;
const EM_SETSEL: UINT = 0x00B1;
const EM_REPLACESEL: UINT = 0x00C2;
const WM_GETTEXTLENGTH: UINT = 0x000E;
const IDI_APPLICATION: LPCSTR = @ptrFromInt(32512);
const IDC_ARROW: LPCSTR = @ptrFromInt(32512);
const COLOR_WINDOW: UINT = 5;

const PROCESSENTRY32W = extern struct {
    dwSize: DWORD,
    cntUsage: DWORD,
    th32ProcessID: DWORD,
    th32DefaultHeapID: usize,
    th32ModuleID: DWORD,
    cntThreads: DWORD,
    th32ParentProcessID: DWORD,
    pcPriClassBase: LONG,
    dwFlags: DWORD,
    szExeFile: [260]u16,
};

const TH32CS_SNAPPROCESS: DWORD = 0x00000002;

const MSG = extern struct {
    hwnd: HWND,
    message: UINT,
    wParam: WPARAM,
    lParam: LPARAM,
    time: DWORD,
    pt: extern struct { x: LONG, y: LONG },
};

const WNDCLASSEXA = extern struct {
    cbSize: UINT,
    style: UINT,
    lpfnWndProc: ?*const fn (HWND, UINT, WPARAM, LPARAM) callconv(.winapi) LRESULT,
    cbClsExtra: i32,
    cbWndExtra: i32,
    hInstance: HINSTANCE,
    hIcon: ?HICON,
    hCursor: ?HCURSOR,
    hbrBackground: HBRUSH,
    lpszMenuName: ?LPCSTR,
    lpszClassName: LPCSTR,
    hIconSm: ?HICON,
};

extern "kernel32" fn GetModuleHandleA(lpModuleName: ?LPCSTR) callconv(.winapi) HINSTANCE;
extern "kernel32" fn CloseHandle(hObject: HANDLE) callconv(.winapi) BOOL;
extern "kernel32" fn CreateToolhelp32Snapshot(dwFlags: DWORD, th32ProcessID: DWORD) callconv(.winapi) HANDLE;
extern "kernel32" fn Process32FirstW(hSnapshot: HANDLE, lppe: *PROCESSENTRY32W) callconv(.winapi) BOOL;
extern "kernel32" fn Process32NextW(hSnapshot: HANDLE, lppe: *PROCESSENTRY32W) callconv(.winapi) BOOL;
extern "kernel32" fn Sleep(dwMilliseconds: DWORD) callconv(.winapi) void;

extern "user32" fn RegisterClassExA(*const WNDCLASSEXA) callconv(.winapi) WORD;
extern "user32" fn CreateWindowExA(dwExStyle: DWORD, lpClassName: LPCSTR, lpWindowName: LPCSTR, dwStyle: DWORD, X: i32, Y: i32, nWidth: i32, nHeight: i32, hWndParent: ?HWND, hMenu: usize, hInstance: HINSTANCE, lpParam: ?LPVOID) callconv(.winapi) ?HWND;
extern "user32" fn DefWindowProcA(hWnd: HWND, msg: UINT, wParam: WPARAM, lParam: LPARAM) callconv(.winapi) LRESULT;
extern "user32" fn GetMessageA(lpMsg: *MSG, hWnd: ?HWND, wMsgFilterMin: UINT, wMsgFilterMax: UINT) callconv(.winapi) BOOL;
extern "user32" fn TranslateMessage(*const MSG) callconv(.winapi) BOOL;
extern "user32" fn DispatchMessageA(*const MSG) callconv(.winapi) LRESULT;
extern "user32" fn ShowWindow(hWnd: HWND, nCmdShow: i32) callconv(.winapi) BOOL;
extern "user32" fn UpdateWindow(hWnd: HWND) callconv(.winapi) BOOL;
extern "user32" fn DestroyWindow(hWnd: HWND) callconv(.winapi) BOOL;
extern "user32" fn PostQuitMessage(nExitCode: i32) callconv(.winapi) void;
extern "user32" fn SendMessageA(hWnd: HWND, msg: UINT, wParam: WPARAM, lParam: LPARAM) callconv(.winapi) LRESULT;
extern "user32" fn SetWindowTextA(hWnd: HWND, lpString: LPCSTR) callconv(.winapi) BOOL;
extern "user32" fn EnableWindow(hWnd: HWND, bEnable: BOOL) callconv(.winapi) BOOL;
extern "user32" fn SetTimer(hWnd: HWND, nIDEvent: usize, uElapse: UINT, lpTimerFunc: ?LPVOID) callconv(.winapi) usize;
extern "user32" fn KillTimer(hWnd: HWND, uIDEvent: usize) callconv(.winapi) BOOL;
extern "user32" fn LoadIconA(hInstance: ?HINSTANCE, lpIconName: LPCSTR) callconv(.winapi) ?HICON;
extern "user32" fn LoadCursorA(hInstance: ?HINSTANCE, lpCursorName: LPCSTR) callconv(.winapi) ?HCURSOR;
extern "user32" fn SetWindowPos(hWnd: HWND, hWndInsertAfter: ?HWND, X: i32, Y: i32, cx: i32, cy: i32, uFlags: UINT) callconv(.winapi) BOOL;

extern "shell32" fn ShellExecuteA(hwnd: ?HWND, lpOperation: LPCSTR, lpFile: LPCSTR, lpParameters: ?LPCSTR, lpDirectory: ?LPCSTR, nShowCmd: i32) callconv(.winapi) usize;

var g_hInst: HINSTANCE = undefined;
var g_hWnd: HWND = undefined;
var g_hStatus: HWND = undefined;
var g_hLog: HWND = undefined;
var g_hBtnStart: HWND = undefined;
var g_hBtnStop: HWND = undefined;
var g_serverRunning = false;

fn LOWORD(dw: UINT) WORD { return @truncate(dw); }

fn logMsg(msg: LPCSTR) void {
    if (@intFromPtr(g_hLog) == 0) return;
    const len = SendMessageA(g_hLog, EM_GETLIMITTEXT, 0, 0);
    if (len > 32000) _ = SetWindowTextA(g_hLog, "");
    const pos = SendMessageA(g_hLog, WM_GETTEXTLENGTH, 0, 0);
    _ = SendMessageA(g_hLog, EM_SETSEL, @intCast(pos), @intCast(pos));
    _ = SendMessageA(g_hLog, EM_REPLACESEL, 0, @as(LPARAM, @intCast(@intFromPtr(msg))));
}

fn processRunning(name: []const u8) bool {
    const s = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (@intFromPtr(s) == std.math.maxInt(usize)) return false;
    defer _ = CloseHandle(s);
    var pe: PROCESSENTRY32W = undefined;
    pe.dwSize = @sizeOf(PROCESSENTRY32W);
    if (Process32FirstW(s, &pe) == 0) return false;
    while (true) {
        var i: usize = 0;
        var match = true;
        while (i < name.len) : (i += 1) {
            var c1 = name[i];
            var c2: u8 = @truncate(pe.szExeFile[i]);
            if (c2 == 0) { match = false; break; }
            if (c1 >= 'a' and c1 <= 'z') c1 -= 32;
            if (c2 >= 'a' and c2 <= 'z') c2 -= 32;
            if (c1 != c2) { match = false; break; }
        }
        if (match and pe.szExeFile[i] == 0) return true;
        if (Process32NextW(s, &pe) == 0) break;
    }
    return false;
}

fn refreshStatus() void {
    g_serverRunning = processRunning("llama-server.exe");
    _ = EnableWindow(g_hBtnStart, if (g_serverRunning) 0 else 1);
    _ = EnableWindow(g_hBtnStop, if (g_serverRunning) 1 else 0);
}

fn wndProc(hWnd: HWND, msg: UINT, wParam: WPARAM, lParam: LPARAM) callconv(.winapi) LRESULT {
    switch (msg) {
        WM_CREATE => {
            g_hWnd = hWnd;
            var y: i32 = 14;
            _ = CreateWindowExA(0, "STATIC", "LLM Server", WS_CHILD | WS_VISIBLE | SS_LEFT, GRP_X, y, GRP_W, 20, hWnd, 0, g_hInst, null);
            y += 24;
            g_hStatus = CreateWindowExA(0, "STATIC", "● Status: Checking...", WS_CHILD | WS_VISIBLE | SS_LEFT, GRP_X + 8, y, GRP_W - 16, 18, hWnd, 0, g_hInst, null).?;
            y += 22;
            _ = CreateWindowExA(0, "STATIC", "Model: Gemma 4 12B QAT + MTP", WS_CHILD | WS_VISIBLE | SS_LEFT, GRP_X + 8, y, GRP_W - 16, 18, hWnd, 0, g_hInst, null);
            y += 22;
            _ = CreateWindowExA(0, "STATIC", "Port: 8080  |  Context: 8192", WS_CHILD | WS_VISIBLE | SS_LEFT, GRP_X + 8, y, GRP_W - 16, 18, hWnd, 0, g_hInst, null);
            y += 30;
            g_hBtnStart = CreateWindowExA(0, "BUTTON", "Start Server", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, GRP_X + 8, y, BTN_W, BTN_H, hWnd, ID_START, g_hInst, null).?;
            g_hBtnStop = CreateWindowExA(0, "BUTTON", "Stop Server", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, GRP_X + 8 + BTN_W + 8, y, BTN_W, BTN_H, hWnd, ID_STOP, g_hInst, null).?;
            y += 42;
            _ = CreateWindowExA(0, "STATIC", "", WS_CHILD | WS_VISIBLE | SS_ETCHEDHORZ, GRP_X, y - 6, GRP_W, 2, hWnd, 0, g_hInst, null);
            y += 10;
            _ = CreateWindowExA(0, "STATIC", "Pipeline", WS_CHILD | WS_VISIBLE | SS_LEFT, GRP_X, y, GRP_W, 20, hWnd, 0, g_hInst, null);
            y += 24;
            _ = CreateWindowExA(0, "STATIC", "Extract tools from YouTube / Google history, categorize", WS_CHILD | WS_VISIBLE | SS_LEFT, GRP_X + 8, y, GRP_W - 16, 18, hWnd, 0, g_hInst, null);
            y += 26;
            _ = CreateWindowExA(0, "BUTTON", "Run Pipeline", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, GRP_X + 8, y, BTN_W, BTN_H, hWnd, ID_RUN, g_hInst, null);
            y += 42;
            _ = CreateWindowExA(0, "STATIC", "", WS_CHILD | WS_VISIBLE | SS_ETCHEDHORZ, GRP_X, y - 6, GRP_W, 2, hWnd, 0, g_hInst, null);
            y += 10;
            _ = CreateWindowExA(0, "STATIC", "Shortcuts", WS_CHILD | WS_VISIBLE | SS_LEFT, GRP_X, y, GRP_W, 20, hWnd, 0, g_hInst, null);
            y += 24;
            _ = CreateWindowExA(0, "BUTTON", "Open Vault", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, GRP_X + 8, y, BTN_W, BTN_H, hWnd, ID_VAULT, g_hInst, null);
            _ = CreateWindowExA(0, "BUTTON", "Open Data", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, GRP_X + 8 + BTN_W + 8, y, BTN_W, BTN_H, hWnd, ID_DATA, g_hInst, null);
            _ = CreateWindowExA(0, "BUTTON", "Open Config", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, GRP_X + 8 + (BTN_W + 8) * 2, y, BTN_W, BTN_H, hWnd, ID_CFG, g_hInst, null);
            y += 42;
            _ = CreateWindowExA(0, "STATIC", "", WS_CHILD | WS_VISIBLE | SS_ETCHEDHORZ, GRP_X, y - 6, GRP_W, 2, hWnd, 0, g_hInst, null);
            y += 10;
            _ = CreateWindowExA(0, "STATIC", "Log", WS_CHILD | WS_VISIBLE | SS_LEFT, GRP_X, y, GRP_W, 20, hWnd, 0, g_hInst, null);
            y += 24;
            const logH = H - y - 50;
            g_hLog = CreateWindowExA(0, "EDIT", "", WS_CHILD | WS_VISIBLE | ES_MULTILINE | ES_READONLY | ES_AUTOVSCROLL | WS_VSCROLL, GRP_X + 8, y, GRP_W - 16, logH, hWnd, 0, g_hInst, null).?;
            _ = CreateWindowExA(0, "BUTTON", "Clear", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, GRP_X + 8, y + logH + 4, 60, 22, hWnd, ID_CLRLOG, g_hInst, null);
            _ = SetTimer(hWnd, ID_TMR, 3000, null);
            refreshStatus();
            logMsg("Dashboard started. Working dir: " ++ BASE);
        },
        WM_COMMAND => {
            const id = LOWORD(@as(UINT, @intCast(wParam)));
            switch (id) {
                ID_START => {
                    _ = ShellExecuteA(null, "open", @ptrCast(@constCast(SERVER_CMD.ptr)), null, null, SW_SHOWNORMAL);
                    logMsg("Starting llama-server...");
                    refreshStatus();
                },
                ID_STOP => {
                    _ = ShellExecuteA(null, "open", "taskkill", "/f /im llama-server.exe", null, SW_HIDE);
                    logMsg("Stopping llama-server...");
                    Sleep(500);
                    refreshStatus();
                },
                ID_RUN => {
                    _ = ShellExecuteA(null, "open", @ptrCast(@constCast(RUN_CMD.ptr)), null, null, SW_SHOWNORMAL);
                    logMsg("Running pipeline...");
                },
                ID_VAULT => _ = ShellExecuteA(null, "open", @ptrCast(@constCast(VAULT_DIR.ptr)), null, null, SW_SHOWNORMAL),
                ID_DATA => _ = ShellExecuteA(null, "open", @ptrCast(@constCast(DATA_DIR.ptr)), null, null, SW_SHOWNORMAL),
                ID_CFG => _ = ShellExecuteA(null, "open", "notepad", @ptrCast(@constCast(CONFIG_FILE.ptr)), null, SW_SHOWNORMAL),
                ID_CLRLOG => _ = SetWindowTextA(g_hLog, ""),
                else => {},
            }
        },
        WM_TIMER => {
            if (wParam == ID_TMR) {
                const was = g_serverRunning;
                refreshStatus();
                if (was != g_serverRunning) logMsg(if (g_serverRunning) "Server online" else "Server offline");
            }
        },
        WM_SIZE => {
            const newW = @as(UINT, @intCast(lParam));
            const w = @as(i32, @intCast(newW & 0xFFFF));
            const h = @as(i32, @intCast((newW >> 16) & 0xFFFF));
            _ = SetWindowPos(g_hLog, null, 0, 0, w - 40, h - 170, SWP_NOMOVE | SWP_NOZORDER);
        },
        WM_CLOSE => _ = DestroyWindow(hWnd),
        WM_DESTROY => { _ = KillTimer(hWnd, ID_TMR); PostQuitMessage(0); },
        else => return DefWindowProcA(hWnd, msg, wParam, lParam),
    }
    return 0;
}

pub fn main() !void {
    g_hInst = GetModuleHandleA(null);
    const cls: LPCSTR = "AIToolCuratorClass";

    var wc = WNDCLASSEXA{
        .cbSize = @sizeOf(WNDCLASSEXA),
        .style = CS_HREDRAW | CS_VREDRAW,
        .lpfnWndProc = wndProc,
        .cbClsExtra = 0,
        .cbWndExtra = 0,
        .hInstance = g_hInst,
        .hIcon = LoadIconA(null, IDI_APPLICATION),
        .hCursor = LoadCursorA(null, IDC_ARROW),
        .hbrBackground = @ptrFromInt(@as(usize, COLOR_WINDOW + 1)),
        .lpszMenuName = null,
        .lpszClassName = cls,
        .hIconSm = null,
    };
    if (RegisterClassExA(&wc) == 0) return error.RegClassFailed;

    const hWnd = (CreateWindowExA(0, cls, "AI Tool Curator Dashboard", WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, W, H, null, 0, g_hInst, null)) orelse return error.CreateWindowFailed;

    _ = ShowWindow(hWnd, SW_SHOWNORMAL);
    _ = UpdateWindow(hWnd);

    var msg: MSG = undefined;
    while (GetMessageA(&msg, null, 0, 0) != 0) {
        _ = TranslateMessage(&msg);
        _ = DispatchMessageA(&msg);
    }
}
