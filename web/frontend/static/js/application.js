let saveData =[];
renderData = [];
if (sessionStorage.getItem('renderData')) {
    let renderData = sessionStorage.getItem('renderData');
} else {
    let renderData = [];
}

document.getElementById('searchButton').addEventListener('click', () => {
    const input = document.getElementById('locationinput');
    if (input.value) {
        //sendData(input.value);
        window.localStorage.clear();
        resetButton();
        applyHiddenClass();
        saveData.push({region : input.value});
        console.log("입력된 지역:", input.value); // 실제로는 원하는 동작으로 변경 가능
    }
});
document.getElementById('locationinput').addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        document.getElementById('searchButton').click();
    }
}); 


const groups = {
    deposit: document.getElementById('depositGroup'),
    rent: document.getElementById('rentGroup'),
    monthRent: document.getElementById('monthrentGroup')
};

const buttons = {
    Rent1 : () => {
        groups.rent.classList.remove('hidden') ;
        groups.deposit.classList.add('hidden');
        groups.monthRent.classList.add('hidden');
        saveData = saveData.map(item => ({
            ...item,
            rentype : '전세'
        }));
        toggleActiveButton('Rent1');
        reset('Rent1')
        saveGroupState();
    },
    Rent2: () => {
        groups.deposit.classList.remove('hidden');
        groups.rent.classList.add('hidden');
        saveData = saveData.map(item => ({
            ...item,
            rentype : '월세'
        }));
        toggleActiveButton('Rent2');
        reset('Rent2')
        saveGroupState();
    },
    depositprice1: () => {
        groups.monthRent.classList.remove('hidden');
        saveData = saveData.map(item => ({
            ...item,
            depositprice : '300만원'
        }));
        toggleActiveButton('depositprice1');
        saveGroupState();
    },
    depositprice2: () => {
        groups.monthRent.classList.remove('hidden');
        saveData = saveData.map(item => ({
            ...item,
            depositprice : '500만원'
        }));
        toggleActiveButton('depositprice2');
        saveGroupState();
    },
    depositprice3: () => {
        groups.monthRent.classList.remove('hidden');
        saveData = saveData.map(item => ({
            ...item,
            depositprice : '1000만원'
        }));
        toggleActiveButton('depositprice3');
        saveGroupState();
    },
    depositprice4: () => {
        groups.monthRent.classList.remove('hidden');
        saveData = saveData.map(item => ({
            ...item,
            depositprice : '5000만원'
        }));
        toggleActiveButton('depositprice4');
        saveGroupState();
    },
    monthprice1: () => {
        saveData = saveData.map(item => ({
            ...item,
            monthprice : '30만원'
        }));                
        toggleActiveButton('monthprice1');
        saveGroupState();
    },
    monthprice2: () => {
        saveData = saveData.map(item => ({
            ...item,
            monthprice : '50만원'
        }));
        toggleActiveButton('monthprice2');
        saveGroupState();
    },
    monthprice3: () => {
        saveData = saveData.map(item => ({
            ...item,
            monthprice : '100만원'
        }));
        toggleActiveButton('monthprice3');
        saveGroupState();
    },
    monthprice4: () => {
        saveData = saveData.map(item => ({
            ...item,
            monthprice : '200만원'
        }));
        toggleActiveButton('monthprice4');
        saveGroupState();
    },
    rentprice1: () => {
        saveData = saveData.map(item => ({
            ...item,
            rentprice : '1억원'
        }));
        toggleActiveButton('rentprice1');
        saveGroupState();
    },
    rentprice2: () => {
        saveData = saveData.map(item => ({
            ...item,
            rentprice : '5억원'
        }));
        toggleActiveButton('rentprice2');
        saveGroupState();
    },
    rentprice3: () => {
        saveData = saveData.map(item => ({
            ...item,
            rentprice : '10억원'
        }));
        toggleActiveButton('rentprice3');
        saveGroupState();
    },
    rentprice4: () => {
        saveData = saveData.map(item => ({
            ...item,
            rentprice : '20억원'
        }));
        toggleActiveButton('rentprice4');
        saveGroupState();
    },
    openScene1Button: () => {
        toggleActiveButton('openScene1Button');
        saveGroupState();
        sessionStorage.setItem('renderData',renderData)
    },
    openScene2Button: () => {
        toggleActiveButton('openScene2Button');
        saveGroupState();
        sessionStorage.setItem('renderData',renderData)
    },
    openScene3Button: () => {
        toggleActiveButton('openScene3Button');
        saveGroupState();
        sessionStorage.setItem('renderData',renderData)
    },
};

// 버튼 클릭 이벤트 리스너 등록
for (const [buttonId, action] of Object.entries(buttons)) {
    const buttonElement = document.getElementById(buttonId);

    buttonElement.addEventListener('click', () => {
        action();

        //sendData(buttonText)
        localStorage.setItem(`buttonState${buttonId}`,buttonElement.classList.contains('activeButton'))
    });
} 

const sceneButtons = [
'openScene1Button',
'openScene2Button',
'openScene3Button',
'openScene4Button'
];

window.onload =() => {
    if (performance.navigation.type === performance.navigation.TYPE_BACK_FORWARD) {
        restoreGroupState();
        loadPriceData();
        for(const [buttonId,action] of Object.entries(buttons)) {
            const state = localStorage.getItem(`buttonState${buttonId}`);
            if (state == 'true') { 
                const buttonGroupPrefix = buttonId.charAt(0);
                const buttonGroup = Object.keys(buttons).filter(buttonId => buttonId.startsWith(buttonGroupPrefix));
                buttonGroup.forEach(buttonId => {
                    document.getElementById(buttonId).classList.remove('hidden')
                })
                document.getElementById('openSceneButton').classList.remove('hidden');
                document.getElementById('openScene4Button').classList.remove('hidden');
                document.getElementById(buttonId).classList.add('activeButton');
            }
        }
    }
    else{
        resetButton();
    }
};

// rent 유형에 따른 버튼 초기화 함수
function reset(clickedButtonId) { 
    const clickedButtonPrefix = clickedButtonId; 
    const activeButtons = [];
    for (const buttonId of Object.keys(buttons)) {
        if (buttonId != clickedButtonPrefix) {
            activeButtons.push(buttonId);
        }
    }
    activeButtons.forEach(buttonId => {
        document.getElementById(buttonId).classList.remove('activeButton');
        localStorage.setItem(`buttonState${buttonId}`, 'false');
    });
}
function resetButton() {
   const activeButtons = document.querySelectorAll('.activeButton');
   activeButtons.forEach(button => {
    button.classList.remove('activeButton');
});
}

const idsToHide = ['depositGroup' ,'monthrentGroup' ,'rentGroup', 'openScene1Button', 'openScene2Button' ,'openScene3Button','openSceneButton','openScene4Button'];

function applyHiddenClass() {
    idsToHide.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.classList.add('hidden'); // hidden 클래스 추가
        }
    });

    console.log("hidden 클래스가 적용되었습니다.");
}

// activeButton 클래스 토글 함수
const sceneopenButtons = {
    ques : document.getElementById('openSceneButton'),
    open1: document.getElementById('openScene1Button'),
    open2: document.getElementById('openScene2Button'),
    open3: document.getElementById('openScene3Button'),
    open4 : document.getElementById('openScene4Button')
};
let lastClickedGroup = '';

function toggleActiveButton(clickedButtonId) {
    const clickedButtonPrefix = clickedButtonId.charAt(0); // 클릭한 버튼의 앞글자
    const activeButtons = [];

    for (const buttonId of Object.keys(buttons)) {
        if (buttonId.charAt(0) === clickedButtonPrefix) {
            activeButtons.push(buttonId);
        }
    }
    // 모든 버튼에서 activeButton 클래스 제거
    const renderbuttons = ['openScene1Button', 'openScene2Button', 'openScene3Button'];
    const isActive = document.getElementById(clickedButtonId).classList.contains('activeButton');
    activeButtons.forEach(buttonId => {
        if (!renderbuttons.includes(buttonId)){
        document.getElementById(buttonId).classList.remove('activeButton');
        localStorage.setItem(`buttonState${buttonId}`, 'false');
        }else{
            if (isActive) {
                document.getElementById(clickedButtonId).classList.remove('activeButton');
                localStorage.setItem(`buttonState${clickedButtonId}`, 'false');
                renderData = renderData.filter(buttonId => buttonId !== clickedButtonId);
            } else{
                document.getElementById(clickedButtonId).classList.add('activeButton');
                localStorage.setItem(`buttonState${clickedButtonId}`,`true`)
                renderData.push(clickedButtonId);
            }
        }
    });
    // 클릭한 버튼에 activeButton 클래스 추가
    if (!renderbuttons.includes(clickedButtonId)){
    document.getElementById(clickedButtonId).classList.add('activeButton');
    localStorage.setItem(`buttonState${clickedButtonId}`,`true`)
    };

    lastClickedGroup = clickedButtonId;
    const sceneElements = document.querySelectorAll('.sceneButton');
    const sceneQuestion = document.querySelector('#openSceneButton');
    const sceneElements2 = document.querySelector('.sceneButton2');
    if (lastClickedGroup.startsWith('rentprice') || lastClickedGroup.startsWith('monthprice') ) {
        document.querySelector('.loading-spinner').classList.remove('hidden')
        document.querySelector('#spinnerText').classList.remove('hidden')
        sendData(saveData)
    } else if(lastClickedGroup.startsWith('open')) {
        /*렌더링 데이터 보내기 코드작성 필요*/
        console.log('클릭된 버튼 주소', renderData)
    }
    
    else {
        sceneElements.forEach(sceneElement => {
            sceneElement.classList.add('hidden'); // 모든 요소에서 hidden 클래스 추가
        });
        sceneElements2.classList.add('hidden')
        sceneQuestion.classList.add('hidden');
    }
    console.log('저장된 데이터',saveData)
}
function saveGroupState() {
    Object.keys(groups).forEach(groupKey => {
        const group = groups[groupKey];
        localStorage.setItem(`${groupKey}Visible`, !group.classList.contains('hidden'));
    });
}
function saveGroupState2() {
    Object.keys(sceneopenButtons).forEach(groupKey => {
        const scenebutton = sceneopenButtons[groupKey];
        localStorage.setItem(`${groupKey}Visible`, !scenebutton.classList.contains('hidden'));
    });
}
// 그룹 상태를 복원하는 함수
function restoreGroupState() {
    Object.keys(groups).forEach(groupKey => {
        const isVisible = localStorage.getItem(`${groupKey}Visible`) === 'true';
        if (isVisible) {
            groups[groupKey].classList.remove('hidden');
        } else {
            groups[groupKey].classList.add('hidden');
        }
    });
    Object.keys(sceneopenButtons).forEach(groupKey => {
        const isVisible2 = localStorage.getItem(`${groupKey}Visible`) ==='true';
        if (isVisible2) {
            sceneopenButtons[groupKey].classList.remove('hidden');
        } else {
            sceneopenButtons[groupKey].classList.add('hidden');
        }
    }) 
}
function goToRenderingPage() { 
    const uniqueRenderData = [...new Set(renderData)]
    const RenderAddress = uniqueRenderData.map(id=> id.match(/\d+/))
    .filter(num=> num!= null).map(num=> num[0]).map(Number).sort((a,b) => a-b);
    let resultAddress;
    if (RenderAddress ===1) {
        resultAddress = `model${RenderAddress[0]}.glb`;
    } else if (RenderAddress.length === 2) {
        if (RenderAddress[0] ===1 && RenderAddress[1] === 2){
            resultAddress =`merged_scene_v1.glb`;
        } else if (RenderAddress[0] ===1 && RenderAddress[1] === 3){
            resultAddress =`merged_scene_v2.glb`;
        }else if (RenderAddress[0] ===2 && RenderAddress[1] === 3){
            resultAddress =`merged_scene_v3.glb`;
            console.log(resultAddress)
        }
    }else{
            resultAddress =`merged_scene_v4.glb`;
        }            
    
    //const resultAddress = `merged_scene_v_${RenderAddress.join('_')}.glb`;
    console.log(resultAddress)
    localStorage.setItem('RenderingImages',resultAddress)
    window.location.href = '/threeDpage'; 

}
function parserPrice(priceString) {
    const parseObject = priceString['가격 '];
    const parts = parseObject.split(" ");
    const type = parts[0];
    const price = parts[1];
    return {type, price};
}
function loadPriceData() {
    fetch('http://127.0.0.1:5000/get_price') 
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data1 => {
        if (data1.success) {
            const result = data1.result
            console.log(result.result1)
            const parsePrice1 = parserPrice(result.result1);
            const parsePrice2 = parserPrice(result.result2);
            const parsePrice3 = parserPrice(result.result3);

            document.getElementById('csvResult1').innerHTML =`${parsePrice1.type} <br> ${parsePrice1.price}`;
            document.getElementById('csvResult2').innerHTML = `${parsePrice2.type} <br> ${parsePrice2.price}`;
            document.getElementById('csvResult3').innerHTML = `${parsePrice3.type} <br> ${parsePrice3.price}`;
        } else {
            console.error('No result found');
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}         
function sendData(inform) {
    fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: inform }),
    })
    .then(response => response.json())
    .then(data => {
        // 결과를 HTML에 표시
        if (data.success){
            loadPriceData(); // 페이지가 로드된 후 데이터 로드
            document.querySelector('.loading-spinner').classList.add('hidden')
            document.querySelector('#spinnerText').classList.add('hidden')
            localStorage.setItem('sceneText',data.result)
            document.getElementById('openSceneButton').classList.remove('hidden');
            document.getElementById('openScene1Button').classList.remove('hidden');
            document.getElementById('openScene2Button').classList.remove('hidden');
            document.getElementById('openScene3Button').classList.remove('hidden');
            document.getElementById('openScene4Button').classList.remove('hidden');  
            document.getElementById('sceneButtonContainer').classList.remove('hidden');
    }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}