
자스에서 따로 어트리 세팅하는 것들이 있는데 헷갈려서.. 
규약이 계속 생기니까, 통일을 주 목적으로 만들어야 할 듯
그리고 리깅 시 도움이 될 만한 기능들 추가.

################################################################################### TMP

x.listRelatives(c=1)[0].getChildren().

x>>y
x//y

listConnections
x.inputs()
x.outputs()

pm.duplicate(pm.ls(sl=1), po=1)

pm.ls('obj*', s=1): # shpaes 만 추출
pm.ls('obj*', tr=1): # transforms 만 추출

################################################################################### ToDo

[ToDo]
- 경로 불러오는 명령어 한 곳에 통일
    - 어덯게??

- Arm, Leg Ctrl 개수 구하는 메소드 따로 만들기?
    ㄴ 리스트로 반환?
    ㄴ 팔이나 다리가 여러개일 경우 많은 기능이 제대로 작동되지 않음 ㅠ
- if Asymmetry correctPV 마저 완성하기
- displayPV 마저 완성하기
- PubCheck: 애니 키 삭제하는 명령어도 추가
- PreRig: leg flatten, IKArm.Follow 추가 (AVSHelp_mir 참고)
- SkinHelpTool: avgSkinTool 되게 수정
    >> /home/jioh.kim/maya/modules/averageVertexSkinWeight/

- UI
    - ui_command: Marking Menu 개발하기
    - 우클릭해서 기능 메뉴 추가하기 ..
    - AVS와 호환되는 기능이면, GSRigTool에서 뭔가 표시되게끔. 추가로 기능이 들어간 버튼은 색깔을 넣든 해서
    - FitSetup부분은 collapse 혹은 삭제

- GS_biped 수정
    - guide nurbs 추가, FitSkeleton.visNurbs 추가 후 연결
        ㄴ build 시에는 unparent 해야됨?
        >> /home/jioh.kim/maya/projects/default/assets/_test/biped/GS_biped_v03.ma
    * GS_biped.ma: TEST_biped_fits.mb 참고하여 수정하기
    * jointCreation 참고
    >> /home/jioh.kim/maya/projects/default/assets/_test/biped/
    - finger Driving System 수정 및 추가
        ㄴ 팀장님이 말씀하신 손가락리깅 중 crunch 등 .. 을 참고하기
        ㄴ AVS - Pose - DrivingSystems - Create Driving System


[RND]
- hipSwinger.translate RND
- MainCtrl, chestIKCtrl 회전 시 spineIK 튀는 이슈 RND
- 팀장님이 말씀하신 손가락 RND
    - scrunch: biped!
    - finger IK: 거미 다리 리깅처럼 손끝이 고정되고 손등만 움직이게끔 리깅
- FitSkeleton 조인트 배치할 때.. biped finger joint 자동으로 맞춰주는 기능 추가? 
    - cluster 말고.. 수석님이 알려주셨던거 잇는데 ... 
    - CGcircuit 강의 참고?
- FKIK switch RND 
    >> 상빈님이 만드심!! 
    >> /gstepasset/WorkLibrary/1.Animation_team/Script/TeamScript/module/picker/

[Toos]
- propRigTool
    - MovableCtrl.. pivot 조정용 컨트롤러 셋팅 ㅇ
        ㄴ negation
        ㄴ Rotate Pivot, Scale Pivot, Rotate Pivot Translate
    - point 4개 찍으면 primary, up vector 반영하여 컨트롤러 등 만들어지는 기능 ㅇ
    - 단추 등 붙이는 것들
    - 커브 -> 조인트, 리그 셋팅: mgear참고, ponyTailRig 로 따로 뺄까?
- SubRigTools
    - folSubRig 점검 및 수정: local-world rig 에도 사용가능하게 수정 
    - ponyTailRigTool
    - skirt/cloak Rig Tool
- autoCarRigTool

[Corrective]
- Rebuild 시 가이드로케이터 따라 위치 수정 안됨
    기존에 있는 것
        - 가이드 로케이터
        - 조인트(스킨)
        - 로케이터(ExtraAttr)
        - Sets
    리빌드 시 ..
        - GetExtraAttr 함수 만들어서 기존 값 들고오기
        - 리깅, 조인트(스킨) 삭제?
        - 재생성, SetExtraAttr 만들어서 값 넣기
- mirror_md 수치값이 잘못됐는지  특정 축을 limit 체크 하면 왼쪽이 오른쪽과 똑같이 따라오지 않음
    - chest_mirror_md 는 다른 파트들과 다른 수치값을 넣어야 할 듯. pos 뿐만 아니라 rot md 도 추가해야 할 듯..
    - limit 수치값들도 ..
- driver가 2개가 될 수 있나 ? Scapula를 Scapula, Shoulder 두 개가 움직이게

[Asymmetry]
- L은 R의 무언가..?를 따라 빌드되기 때문에 오차범위가 클수록 서로 축이 다르게 만들어짐

[Errors]
- 최초로 maya를 열었을 때에는(avs 가 아직 실행되지 않은 경우) avs 명령어가 실행되지 않음. 
    >> AVS open하는 버튼 만듦

################################################################################### Daily

230531
- RigHelp 마저 완성
    - UI: attribute
    - 기능: Constraint, Connect, Lock, Parent, attr
- CopySkin 이슈
    - shapeOrig1 생기는 이슈
    - 같은 조인트로만 되는 이슈
- AverageSkinWeights: vtx 선택시 실행안됨

230526
- propRigTool
    - kk controllers 기능 추가
    - 컬러 팔레트 추가
    - vtxRig: 컨트롤러 생성 전 수동으로 조금 조절할 수 있게 guide(locator) 생성 후, 리그 만들기

230525
- propRigTool
    - vtx 4개 선택해서 서브리깅 만드는 기능 추가
    - movable pivot ctrl 기능 추가
- Build 버튼 우클릭 시 PreRig 나타나게? 아니면 다른 곳? 

230519
- Corrective Rig 수정
    - rebuild 코드 수정
    - getExtraAttr, getLimitAttr > setAttr 기능 추가하기
- Build 버튼에 PreRigRun 추가, PreRig 버튼은 삭제

230509
- GS_biped 수정
    - 추가된 fit Setup 세팅 GS_biped 에도 추가 수정 
    - MiddleFinger, ToeEnd 가 각 상위 조인트의 첫번째 하위로 가게 수정: 그 조인트로 축이 따라감 
    - Cup 삭제하고, *Finger0 을 추가
    - autoOrient Finger 수정
    - ankle, toe 축 세팅 수정 
    - 조인트(가이드) 사용하면 안되는 어트리는 Lock 시키기
- SkinHelpTool
    - vertex 다중 선택 시 interactive,post 다중실행되는 것 .. 한번만 실행되도록 수정
    - copySkin 기능 안되는것 수정

230508
- UI: pymel.popupMenu(markingMenu) 
    >> 포기
- Core
    - FitSetup: if문 추가
    - Auto-Orient시 Finger은 영향 안받게

230504
- skinHelpTool: post/interactive 호환 버튼 추가
- Core: List에 item 추가하는거 함수 하나로 정리..
- UI: frameLayout.collapse: Sub, Other
    >> /gstepasset/WorkLibrary/1.Animation_team/Script/_forRigger/GSRigTool/util/ui_commands


230503
- RigHelp 그룹박스 가독성
- FitSetup: Ankle.worldOrient: AVS 업데이트에 맞춰서 worldOrientUp.Forward 으로 수정

230502
- Core
    - IKSubPart: 다리에도 추가되게, 여러개여도 추가되게, 중복으로 추가되지 않게 
    - 상수대리님 osGrp UI 추가
- propRigTool 만들기
    - Create Base Rig: Milki + MainSystem

230428
- colorMaker 기능 안됨: proc > global proc 으로 수정

230427
- Auto-Orient: Scapula.jointOrient 추가
- switchAllFKIK 추가
- Ctrl 수치값 디폴트로 만드는 기능.버튼 생성, PubCheck에 추가

230426
- GSRigTool_install 완성하기. AVS 처럼 drag and drop 으로 설치되게
- 팔/다리가 여러개일 경우 대응되게 스크립트 수정
    - IKSubArm
    - PubCheck
    - 그 외 점검..

230425
- mainCtrl 네이밍 수정
    >> Main, Globe, World
- import biped, Auto-Orient을 Fit setup과 합친 버튼 추가
    >> importGSBiped
- FitSetup.Shoulder에 ikLocal 추가
- RigHelp에 skinCopy를 합칠까?? 그럼 listWidget 하나만 있어도 되는데
    >> ㄴㄴ 팀원분들이 용도대로 분리돼있는게 좋을것같다고 하심
- 완성안된 ui들 제외하고 임시완료파일 배포 
- 팔/다리가 여러개일 경우 대응되게 스크립트 수정
    - FitSetup
    - AsymmetrySetup
    
230424
- mayaDockable 수정 끝내기
    >> ui.py 가 아니라 run.py(최종) 에서 dockable window로 wrap 해야 함
- skinHelpTool.skinCopy 기능 마저 만들기
- Rig Help UI 추가 중

230421
- 툴들 공통 기능, 자주 사용하는 기능 등 수정/편집
    - skinHelpTool 만드는중
    - mayaDockable 되게 수정 중

230420
- deformeIssue 스크립트로 수정 좀 하고 추가시키기
- UI tab 나누기
- 툴, 스크립트들 추가
    - rename tool
    - folSubRigTool
    - osGrp
    - JHTool
    - fixHeadSquash
    - HIK setup
    - 상빈님이 주신거 추가: skinTool, simpleRigTool, ctrlCtl

230419
- undo an entire function call
- pubCheck - optimizeSceneSize 추가

230418
- Auto-Orient
    Auto-Orient 버튼 누르면: Y/Z, Auto-Orient(wrist, finger)
    Build 전엔 Y/X 으로 수정
- Pre Rig 기능들.. 선택적으로 할 수 있게 수정하기. AVS의 keepAll 처럼

230417
- Corrective가 Toggle/Rebuild 에 대응되게 수정

230414
- GSRigTool 에 CorrectiveRig 추가 중..

230413
- GSRigTool_Core.py 수정
- 이름을 Slide 에서 Corrective 으로 변경
- Asymmetry 일 때, guide 정리 코드 추가해야 함
	>> setSlideGuide / 아니면 새 함수 만들기

230412
- CorrectiveJntRig 기능 추가 및 기타..

230327
- Asymmetry: (Scapular, Hip, Eye 중) 선택적으로 없어도 실행되게 ??
- UI에 LRA, PoleVec vis checkBox 추가


230327
- ifAsymmetryBuild

230323
- spine joint resample
- UI에 Auto-Orient 추가 / 디폴트를 Y,Z





