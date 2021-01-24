import win32com.client as win32
import time

hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.Open("C:/automation_hwp/example.hwp",hwp,hwp)

'''
백그라운드의 아래아한글, 숨김해제(파이썬으로 한글 오픈시 백그라운드가 기본설정) 
백그라운드에 먼저 열려 있는경우 읽기 전용으로 열리므로
Ctrl-Shift-Esc 눌러서 작업관리자에서 백그라운드 프로세스 중에 hwp 있으면 우클릭해서 다 종료
'''
current_window = hwp.XHwpWindows.Item(0)
current_window.Visible = True

"""모든 수식 텍스트 차례로 dict로 얻기.
키는 (List, Para, Pos), 값은 eqn_string"""
def extract_eqn(hwp): # 이전 포스팅에서 소개한, 수식 추출방법을 함수로 정의
    Act = hwp.CreateAction("EquationModify") # Action 객체를 생성한다. 액션에 대한 세부적인 제어가 필요할 때 사용한다
    Set = Act.CreateSet() # parameter set 생성. 어떤 Action들은 그 Action이 수행되기 위해서 정보가 필요한데 이때 사용되는 정보를 ParameterSet으로 넘겨준다
    Pset = Set.CreateItemSet("EqEdit", "EqEdit") # 아이템으로 parameter set을 생성한다.
    Act.GetDefault(Pset) # parameter set 초기화
    return Pset.Item("String") # 지정한 아이템의 값을 반환하다. 

eqn_dict = {} # 사전 형식의 자료 생성 예정
ctrl = hwp.HeadCtrl # 첫 번째 컨트롤(HeadCtrl)부터 탐색 시작.

while ctrl != None: # 끝까지 탐색을 마치면 ctrl이 None을 리턴하므로.
    nextctrl = ctrl.Next # 미리 nextctrl을 지정해 두고,
    if ctrl.CtrlID == "eqed": # 현재 컨트롤이 "수식eqed"인 경우
        position = ctrl.GetAnchorPos(0) # 해당 컨트롤의 좌표를 position 변수에 저장
        position = position.Item("List"), position.Item("Para"), position.Item("Pos")
        hwp.SetPos(*position) # 해당 컨트롤 앞으로 캐럿(커서)을 옮김
        hwp.FindCtrl() # 해당 컨트롤 선택
        time.sleep(1) # 시연을 위해 1초 멈춤
        eqn_string = extract_eqn(hwp).rstrip() # 문자열 추출, rstrip 문자열의 오른쪽에 있는 공백을 제거

        if eqn_string[-1] != "`":
            eqn_string = eqn_string + "`"    
            hwp.Run("Select") # 선택
            hwp.Run("Erase") # 지우기
            hwp.HAction.GetDefault("EquationCreate", hwp.HParameterSet.HEqEdit.HSet)
            hwp.HParameterSet.HEqEdit.string = eqn_string
            hwp.HAction.Execute("EquationCreate", hwp.HParameterSet.HEqEdit.HSet) # 폰트이상함
            hwp.FindCtrl() # 다시 선택
            hwp.HAction.GetDefault("EquationPropertyDialog", hwp.HParameterSet.HShapeObject.HSet)
            hwp.HParameterSet.HShapeObject.HSet.SetItem("ShapeType", 3)
            hwp.HParameterSet.HShapeObject.Version = "Equation Version 60"
            hwp.HParameterSet.HShapeObject.EqFontName = "HYhwpEQ"
            hwp.HParameterSet.HShapeObject.HSet.SetItem("ApplyTo", 0)
            hwp.HParameterSet.HShapeObject.HSet.SetItem("TreatAsChar", 1)
            hwp.HAction.Execute("EquationPropertyDialog", hwp.HParameterSet.HShapeObject.HSet)
            hwp.Run("Cancel") # 폰트 예뻐짐
            hwp.Run("MoveRight") # 다음 수식 삽입 준비

        eqn_dict[position] = eqn_string # 좌표가 key이고, 수식문자열이 value인 사전 생성
    ctrl = nextctrl # 다음 컨트롤 탐색
hwp.Run("Cancel") # 완료했으면 선택해제
hwp.SaveAs("C:/automation_hwp/example1.hwp", "HWP") # 파일을 다른이름 저장하고 나갑니다. 
hwp.Quit()


