var HachiJRPG = HachiJRPG || {};

//title screen
HachiJRPG.Game = function(){};

HachiJRPG.Game.prototype = {
  init: function(paramArr) {    
    this.saveslot = paramArr[0];
    this.hero = playerData[this.saveslot];
    this.settings = playerData.settings;
    this.texto = this.game.cache.getJSON('uitext'); //this.texto[language]["chave"]
    this.enredo = this.game.cache.getJSON('plot'); //this.enredo[language]["grupo"]["chave"]
    this.dungeon = this.game.cache.getJSON('dungeon'); //this.dungeon["level"+this.hero.level]["chave"]
    this.enemy = this.game.cache.getJSON('monsters'); //this.enemy["level"+this.hero.level][indice]["chave"]
    this.bosses = this.game.cache.getJSON('bosses'); //this.bosses[indice]["chave"]
    this.items = this.game.cache.getJSON('items'); //this.items[page]["chave"]
    //console.log(this.settings);
  },
  
  preload: function() {},
  
  create: function() {

    this.crossFadeBitmap = this.game.make.bitmapData(this.game.width, this.game.height);
    this.crossFadeBitmap.rect(0, 0, this.game.width, this.game.height, "rgb(255,0,0)");
    this.dmgOverlay = this.game.add.sprite(this.game.camera.x,this.game.camera.y, this.crossFadeBitmap);
    this.dmgOverlay.visible = false;

    this.dgimg = this.game.add.sprite(0, 0, 'dungeonScene');
    this.bgimg = this.game.add.sprite(0, 0, 'villageScene');

    this.villageFade = this.game.add.tween(this.bgimg);
    this.villageFade.to({alpha:0},2000);
    this.villageFade.onComplete.add(this.startExploration,this);
	/*TODO: Usar a linha abaixo para iniciar a exploração da dungeon*/
    //this.villageFade.onComplete.add(this.generateDungeon,this);

    this.villageShow = this.game.add.tween(this.bgimg);
    this.villageShow.to({alpha:1},2000);
    this.villageShow.onComplete.add(this.showButtons,this);
    
    // Game variables
    this.paused = false;
    this.gameover = false;
    this.showingMessage = false;
    this.wave = 0;
    this.maxwave = 0; 
    this.expwave = 0;
    this.goldwave = 0;
    this.bossmode = false; 
    this.reward = "";
        
    /******** Sprites creation ********/
    
    // UI creation
    this.heroWindowSmall = new HeroWindowSmall(this.game,this.hero,this);

    //Objetos
    
    //Botões
    /*this.dungeonButton = this.game.add.button(this.game.world.centerX - 128, this.game.height-80, 'icons64', this.villageFadeAction, this, 0, 0, 0);
    this.innButton = this.game.add.button(this.game.world.centerX - 48, this.game.height-80, 'icons64', this.innEvent, this, 3, 3, 3);
    this.shopButton = this.game.add.button(this.game.world.centerX + 48, this.game.height-80, 'icons64', this.setShopWindow, this, 1, 1, 1);
    this.tavernButton = this.game.add.button(this.game.world.centerX + 128, this.game.height-80, 'icons64', this.setTavernScene, this, 2, 2, 2);
    //this.debugButton = this.game.add.button(this.game.width - 64, this.game.world.centerY, 'icons64', this.debugLvUp, this, 2, 2, 2);
    this.dungeonButton.anchor.setTo(0.5,0);
    this.innButton.anchor.setTo(0.5,0);
    this.shopButton.anchor.setTo(0.5,0);
    this.tavernButton.anchor.setTo(0.5,0);*/
    this.optionsButton = this.game.add.button(this.game.width - 32, 0, 'icons32', this.openOptions, this, 2, 2, 2);
    
    //Janelas fixas
    this.battleWindow = new BattleWindow(this.game,this.hero,this);
    this.treasureWindow = new TreasureWindow(this.game,this.hero,this);
    this.expWindow = new ExpWindow(this.game,this.hero,this);
    this.messageWindow = new MessageWindow(this.game,this);
    this.townsystem = new TownSystem(this.game,this);
    this.tavernsystem = new TavernSystem(this.game,this);
    this.eventsystem = new EventSystem(this.game,this);
	//this.dungeonsystem = new DungeonSystem(this.game,this);

    this.heroWindow = new HeroWindow(this.game,this.hero,this);
    this.game.add.existing(this.heroWindow);
    this.shopWindow = new ShopWindow(this.game,this.hero,this);
    
    this.crossBitmap = this.game.make.bitmapData(this.game.width, this.game.height);
    this.crossBitmap.rect(0, 0, this.game.width, this.game.height, "rgb(0,0,0)");
    this.overlay = this.game.add.sprite(this.game.camera.x,this.game.camera.y, this.crossBitmap);
    this.overlay.alpha = 0;
    
    /*****************************
     ******** GAME SOUNDS ********
     *****************************/
    /* this.pinSound = this.game.add.audio('pinhit');
    this.rollSound = this.game.add.audio('rolling');
    this.skullSound = this.game.add.audio('explode');
    this.selectSound = this.game.add.audio('select');
    this.cancelSound = this.game.add.audio('cancel');
    this.powerSound = this.game.add.audio('powerup');
    this.overSound = this.game.add.audio('over');
    this.coinSound = this.game.add.audio('coin'); */
    this.bgmtown = this.game.add.audio('bgmtown', 1, true);
    this.bgmdungeon = this.game.add.audio('bgmdungeon', 1, true);
    this.bgmbattle = this.game.add.audio('bgmbattle', 1, true);
    this.bgmboss = this.game.add.audio('bgmboss', 1, true);
    if(bgmOn) {
      if (currentBGM!= '') currentBGM.stop();
      currentBGM = this.bgmtown;
      currentBGM.play();
      isPlayingBGM = true;
    }

    /****************************
     ********** TIMERS **********
     ****************************/
    //invocados nas batalhas
	this.removeFlickerTimer = this.game.time.create(false);
    this.flickTimer = this.game.time.create(false);
    
    //Registrando input na tela
    this.game.input.onDown.add(this.handlePointerDown,this);

    //Caso o jogador esteja começando um novo jogo, exibir mensagem de boas vindas, caso contrário exibir um bem vindo de volta
    this.hideButtons();
    if (this.hero.newgame == true){
      this.messageWindow.showMensagem([ //welcome
        this.enredo[language]["welcome"]["1"],
        this.enredo[language]["welcome"]["2"],
        this.enredo[language]["welcome"]["3"],
        this.enredo[language]["welcome"]["4"],
        this.enredo[language]["welcome"]["5"],
        this.enredo[language]["welcome"]["6"],
        this.enredo[language]["welcome"]["7"],
        this.enredo[language]["welcome"]["8"],
      ],
      function(context){
        context.hero.newgame = false;
        context.showButtons(false);
      });
    }else{
      this.messageWindow.showMensagem([ //welcomeback
        this.enredo[language]["welcomeback"]["1"],
        this.enredo[language]["welcomeback"]["2"],
        this.enredo[language]["welcomeback"]["3"],
        this.enredo[language]["welcomeback"]["4"],
      ],
      function(context){
        context.showButtons(false);
      });
    }
  },
  
  update: function() {
    //button presses will be processed here
    
    // Updating UI information
    this.heroWindowSmall.updateInfo(this.hero);
    if(this.heroWindow.visible){
      this.heroWindow.updateInfo(this.hero);
    }
    if(this.battleWindow.visible){
      this.battleWindow.updateInfo(this.hero);
    }
    if(this.treasureWindow.visible){
      this.treasureWindow.updateInfo(this.hero);
    }
  },
  
  render: function(){
    // this.game.debug.text("HERO: " + this.hero.name + " New: " + this.hero.newgame, 0, 10);
    // this.game.debug.text("HP: " + this.hero.hp + "|TP: " + this.hero.tp + "|GOLD: " + this.hero.gold, 0, 20);
    // this.game.debug.geom( this.ball.getBounds(), 'rgba(255,255,0,0.4)' ) ;
    // this.game.debug.geom( this.block1.getBounds(), 'rgba(255,0,255,0.4)' ) ;
  },
  
  handlePointerDown: function(pointer){
    if(this.testWindowsVisible()){
      if(this.battleWindow.visible){
        this.battleWindow.atualizaMensagem(this);
      }
      if(this.treasureWindow.visible){
        this.treasureWindow.atualizaMensagem(this);
      }
    }else{
      if(this.messageWindow.visible){
        this.messageWindow.atualizaMensagem();
      }
    }

    if (!this.eventsystem.angleBar.angleset) this.eventsystem.stopCursor();
  },

  testWindowsVisible: function(){
    return (this.battleWindow.visible || this.treasureWindow.visible);
  },

  hideButtons: function(){
    /*this.dungeonButton.visible = false;
    this.innButton.visible = false;
    this.shopButton.visible = false;
    this.tavernButton.visible = false;*/
    this.townsystem.close();
  },

  showButtons: function(playbgm){
    if(typeof playbgm == 'undefined') playbgm = true;
    this.townsystem.start();
    this.saveGame();
    
    if(bgmOn && playbgm) {
      currentBGM.stop();
      currentBGM = this.bgmtown;
      currentBGM.restart('', 0, 1, true);
      currentBGM.play();
      isPlayingBGM = true;
    }
  },

  flickerScreen: function() {
    this.dmgOverlay.visible = !this.dmgOverlay.visible;
  },

  removeFlicker: function(){
    this.flickTimer.stop();
    this.dmgOverlay.visible = false;
  },

  startDamageFlicker: function(){
    this.removeFlickerTimer.add(1200, this.removeFlicker, this);
    this.flickTimer.loop(200, this.flickerScreen, this);     
    this.removeFlickerTimer.start();
    this.flickTimer.start();
  },
  
  /*Dungeon Methods*/
  generateDungeon: function(){
	var floor = this.dungeon["level"+this.hero.floor];
	var dungeon = floor.challenges;
	
	//cada andar terá 6 salas, com exceção do último andar
	if (this.hero.floor < global_dragonLevel){
	  dungeon.sort(function(a, b){return 0.5 - Math.random()}); //https://www.w3schools.com/js/tryit.asp?filename=tryjs_array_sort_random
	}else{
	  dungeon = ["battle"]; //apenas uma sala, onde se encontra o Dragão
	}
	console.log(this.dungeon);
	//this.dungeonsystem.setFloor(dungeon)
  }

  resumeExploration: function(beatfloor){    
    if (this.wave>=this.maxwave){
      var floor = this.dungeon["level"+this.hero.floor];
      var args = {bonusexp: floor.bonusexp, bonusgold: floor.bonusgold, upstairs: beatfloor};
      this.wave = 0;
      this.messageWindow.args = args;
      var endmessage = beatfloor ? "finishexploring" : "returnhome";
      
      this.messageWindow.showMensagem([
        this.texto[language][endmessage].replace('VAREXPREWARD',floor.bonusexp).replace('VARGOLDREWARD',floor.bonusgold)
      ],
      function(context,args){
        if (args.upstairs) {
          context.hero.floor+=1;
          if(context.hero.floor > context.hero.maxfloor)
            context.hero.maxfloor = context.hero.floor;
          /*context.hero.exp += args.bonusexp;
          context.hero.gold += args.bonusgold;
          if(context.checkLevelUp()==true){
            context.expWindow.visible = true;
          }else{            
            context.showButtons();
          }*/
        }//else{
        context.endExploration();
        //}
      });
    }else if(this.wave>0){
      this.startExploration();
    }else{
      this.endExploration();
    }
  },

  villageFadeAction: function(){
    this.hideButtons();
    this.villageFade.start();
    if(bgmOn) {
      currentBGM.fadeOut(1800);
      isPlayingBGM = false;
    }
  },

  endExploration: function(){
    this.villageShow.start();
    if(bgmOn) {
      currentBGM.fadeOut(1800);
      isPlayingBGM = false;
    }
  },

  startExploration: function(){
    if (this.paused){
      return false;
    }

    this.hideButtons();
    
	//Define qtd de waves para a aventura
    if (this.wave == 0){
      var floor = this.dungeon["level"+this.hero.floor];
      this.wave = 1;
      this.maxwave = floor.maxwave;
    }else{
      this.wave++;
    }
    
    if (!isPlayingBGM){
      isPlayingBGM = true;
      if(bgmOn) {
        currentBGM.stop();
        currentBGM = this.bgmdungeon;
        currentBGM.restart('', 0, 1, true);
        currentBGM.play();
      }
    }
    
	/*TODO: criar um prefab dungeonsystem, onde informa ao jogador uma janela com escolha de rooms*/
	/**
	 * this.dungeonsystem.showRooms()
	 * Ao escolher uma sala, o dungeonsystem deve substituir a sala por "none", que indica não ter nada por lá 
	 * -----
	 * sala1
	 * sala2
	 * salan
	 * 
	 * itens
	 * orar
	 * voltar
	 */
    this.messageWindow.showMensagem([
      this.texto[language]["exploringdungeon"]
    ],
    function(context){
      context.exploreDungeon();
    });
  },
  
  /**
   * Esta função gera a quest, disparando os desafios de acordo com a wave atual
   * para 1 e 4: 5 chances batalha e 1 tesouro
   * para 3: 4 chances de batalha e 2 de tesouro
   * para 2: 4 chances de tesouro e 2 batalha
   * para 5 à 7: somente batalha
   * 
   * TODO: reformular este método, usando o dungeonsystem para definir o que ocorrerá diante da sala escolhida
   */
  exploreDungeon: function(){
    var floor = this.hero.floor;
    //var level = rollDice(floor);
    var events = ['battle','battle','battle','battle','battle','event'];
    //var events = ['event','event','event','event','event','event'];
    switch(this.wave){
      case 2: events = ['event','event','event','event','event','battle']; break;
      case 3: events = ['battle','battle','event','event','battle','battle']; break;
      case 5: events = ['battle','battle','battle','battle','battle','event']; break;
      case 6: events = ['battle','battle','event','battle','battle','event']; break;
      case 7: events = ['battle','battle','battle','battle','battle','battle']; break;
    }

    if (this.checkSideQuest() == true) return;

    //TODO: Decidir pela wave que desafio liberar (criar um esquema q dificulta com a evolução da wave)
    var dice = rollDice(6) - 1;      
    switch(events[dice]){
      case 'battle': this.setBattleWindow(floor); break;
      case 'event': this.setEventChallenge(floor); break;
      //case 'none': this.setNoneEvent(floor); break;
    }      
  },
  
  setNoneEvent: function(){
	this.messageWindow.showMensagem([
      this.texto[language]["emptyroom"] //TODO: criar tradução para essa label
    ],
    function(context){
      context.setExpWindow();
    });
  }

  checkSideQuest: function(){
    var floor = this.dungeon["level"+this.hero.floor];
    if (this.wave!=floor.secretwave) return false;

    if(floor.secret == 1 && typeof this.hero.itens[floor.secretreward] == 'undefined'){
      var condition = floor.condition.split("|");
      switch(condition[0]){
        case "phi": case "dex": case "kno": 
          console.log('indo para o custom challenge');
          this.setEventCustomChallenge(floor.challengeid);
          return true;
          //break;
        case "boss": 
          var bonus = 0;
          if (this.hero[floor.conditionbonus] > 0) 
            bonus = this.hero[floor.conditionbonus];
          
          console.log(this.hero[condition[2]] + bonus +" vs "+ condition[3]);
          if (this.hero[condition[2]] + bonus >= condition[3]){
            //this.wave = 1;
            //this.maxwave = 1;
            this.setBossWindow(condition[1],floor.secretreward);
            return true;
          }
          break;
        case "jewels": 
          if (this.hero.itens.swordjewel > 0 || this.hero.itens.shieldjewel > 0 ||
              this.hero.itens.toolsjewel > 0 || this.hero.itens.bookjewel > 0){
            this.completeJewelQuest();
            return true;
          }
          break;
        case "final": 
          //TODO: marcar que ao derrotar o dragão, é preciso enfrentar a Nicky logo em seguida
          this.setBossWindow(condition[1],floor.secretreward);
          return true;
          //break;
      }
    }

    return false;
  },

  giveJewelToPlayer(reward){
    console.log(reward);
    this.messageWindow.args = reward;    
    console.log(this.messageWindow.args);
    this.messageWindow.showMensagem([
      this.enredo[language][reward]["1"],
      this.enredo[language][reward]["2"],
      this.enredo[language][reward]["3"],
      this.enredo[language][reward]["4"],
    ],
    function(context,args){
      context.hero.itens[args] = 1;
      console.log(args);
      context.setExpWindow();
    });
  },

  completeJewelQuest(){
    var message = [
      this.enredo[language]["completejewelquest"]["1"],
      this.enredo[language]["completejewelquest"]["2"],
      this.enredo[language]["completejewelquest"]["3"],
      this.enredo[language]["completejewelquest"]["4"],
      this.enredo[language]["completejewelquest"]["5"],
    ];
        
    if (typeof this.hero.itens.toolsjewel != 'undefined' && this.hero.itens.toolsjewel > 0){
      console.log('giving tools');
      this.hero.itens.toolsjewel = 0;
      this.hero.tool_id = 7;
      message.push(this.enredo[language]["completejewelquest"]["6"]);
    }
    
    if (typeof this.hero.itens.shieldjewel != 'undefined' && this.hero.itens.shieldjewel > 0){
      console.log('giving shield');
      this.hero.itens.shieldjewel = 0;
      this.hero.shield_id = 7;
      message.push(this.enredo[language]["completejewelquest"]["7"]);
    }

    if (typeof this.hero.itens.swordjewel != 'undefined' && this.hero.itens.swordjewel > 0){
      console.log('giving sword');
      this.hero.itens.swordjewel = 0;
      this.hero.weapon_id = 7;
      message.push(this.enredo[language]["completejewelquest"]["8"]);
    } 
    
    if (typeof this.hero.itens.bookjewel != 'undefined' && this.hero.itens.bookjewel > 0){
      console.log('giving book');
      this.hero.itens.bookjewel = 0;
      this.hero.book_id = 7;
      message.push(this.enredo[language]["completejewelquest"]["9"]);
    }
    
    this.messageWindow.showMensagem(message,
    function(context){
      context.setExpWindow();
    });
  },

  setBattleWindow: function(level){
    var floor = this.dungeon["level"+level];
    var qtdmonstros = floor.monsters;
      
    var idxmonstro = rollDice(qtdmonstros.length) - 1;
    switch (this.wave){
      case 1: case 2: if (idxmonstro >= 2) idxmonstro = rollDice(2) - 1; /*if (level > 1) level-=(rollDice(2) - 1);*/ break;
      case 3: case 4: case 5: if (idxmonstro < 2) idxmonstro = rollDice(2) + 1; break;
      case 6: case 7: idxmonstro = 3; break;
    }
    var enemy = this.enemy[floor.monsters[idxmonstro]];

    /*var handicap = this.hero.level - enemy.level;
    if (handicap > 0){ //Level up monster
      while (handicap > 0){
        dice = rollDice(4);
        switch(dice){
          case 1: case 2: enemy.phi += 1; break;
          case 3: enemy.dex +=1; break;
          case 4: enemy.kno +=1; break;
        }
        enemy.gold += rollDice(10);
        enemy.exp += rollDice(6);
        enemy.hp += 5;
        handicap--;
      }
    }
    
    console.log(enemy);*/
    this.battleWindow.visible = true;
    this.battleWindow.startBattle(enemy);
    
    if(bgmOn) {
      currentBGM.stop();
      currentBGM = enemy.name != 'NICKY' ? this.bgmbattle : this.bgmboss;
      currentBGM.restart('', 0, 1, true);
      currentBGM.play();
      isPlayingBGM = true;
    }
  },

  setBossWindow: function(index,reward){
    var enemy = this.bosses[index];
    console.log(enemy);
    
    this.bossmode = true; 
    this.reward = reward; 
    this.battleWindow.visible = true;
    this.battleWindow.startBattle(enemy);
  },

  seTreasureWindow: function(level){
    var difficulty = (5 * Math.ceil(level/3)) +5;
    var chances = rollDice(4);
    console.log(difficulty);

    this.treasureWindow.visible = true;
    this.treasureWindow.startTest(chances,difficulty);
  },

  setEventChallenge: function(level){
    this.eventsystem.challengePlayer(level);
  },

  setEventCustomChallenge: function(challengeID){
    this.eventsystem.challengeCustom(challengeID,this.hero.floor);
  },

  checkLevelUp(){
    var targetexp = nextLevelDnD(this.hero.level,global_baseExp,global_expoent);
    if(this.hero.exp >= targetexp){
      return true;
    }
    return false;
  },
  
  setExpWindow: function(){
    if(this.hero.hp > 0){
      if(this.bossmode == true){
        this.bossmode = false; 
        if(this.reward == "finalboss"){
          this.messageWindow.showMensagem([ //finalboss: encontro com a Nicky
            this.enredo[language]["finalboss"]["1"],
            this.enredo[language]["finalboss"]["2"],
            this.enredo[language]["finalboss"]["3"],
            this.enredo[language]["finalboss"]["4"],
            this.enredo[language]["finalboss"]["5"],
            this.enredo[language]["finalboss"]["6"],
            this.enredo[language]["finalboss"]["7"],
            this.enredo[language]["finalboss"]["8"],
            this.enredo[language]["finalboss"]["9"],
            this.enredo[language]["finalboss"]["10"],
          ],
          function(context){
            //context.hero.gold = 100 * lastlevel;
            context.setBossWindow(2,"endgame");
          });
          return;
        }else if(this.reward == "endgame"){
          this.finishGame();
          return;
        }else if (this.reward!= ""){
          this.giveJewelToPlayer(this.reward);
          this.reward = "";
          return;
        }
      }

      this.hero.exp += this.expwave;
      if (this.hero.gold <= 99999) this.hero.gold += this.goldwave;
      this.expwave = this.goldwave = 0;
      if(this.checkLevelUp()==true){
        this.expWindow.open();
        return;
      }
      
      if(this.wave < this.maxwave){
        this.keepAdventuring = new ChoiceWindow(this.game,this.texto[language]["keepexploringquestion"],this,
          this.texto[language]["yes"],this.texto[language]["no"],
          function(){
            if(sfxOn===true){
              this.selectSound.play();
            }
            this.resumeExploration(false);
            this.keepAdventuring.destroy();
            //this.overlay.alpha = 0;
          },
          function(){
            if(sfxOn===true){
              this.cancelSound.play();
            }
            this.wave = this.maxwave;
            this.resumeExploration(false);
            this.keepAdventuring.destroy();
            //this.overlay.alpha = 0;
          }
        );
      }else{
        this.resumeExploration(true);
      }
    }else{
      /*if (this.hero.itens.potion >= 1){
        var message = this.itemEvent("potion");
        this.messageWindow.showMensagem([message],
          function(context){
            context.setExpWindow();
          }
        );
      }else{*/
        this.messageWindow.showMensagem([ //respawn
          this.texto[language]["gamelost"]
        ],
        function(context){
          context.respawnEvent();
        });
      //}
    }
  },

  respawnEvent: function(){
    this.resetHero();
    this.messageWindow.showMensagem([ //respawn
      '...',
      '.....',
      '.......!',
      this.enredo[language]["respawn"]["1"],
      this.enredo[language]["respawn"]["2"],
      this.enredo[language]["respawn"]["3"],
      this.enredo[language]["respawn"]["4"],
      this.enredo[language]["respawn"]["5"],
      this.enredo[language]["respawn"]["6"],
      this.enredo[language]["respawn"]["7"],
      this.enredo[language]["respawn"]["8"],
      this.enredo[language]["respawn"]["9"],
    ],
    function(context){
      context.hero.gold = 100;
      context.endExploration();
    });
  },

  itemEvent: function(item,showmessage){
    if (typeof showmessage == 'undefined') showmessage = true;
    var message = '';
    this.phase = 'playerturn';
    switch (item){
      case "potion":
        this.hero.itens.potion -= 1;
        var increase = 14 + rollDice(6);
        this.hero.hp += increase;
        if (this.hero.hp > this.hero.maxhp) this.hero.hp = this.hero.maxhp;
        message = this.hero.name+this.texto[language]["battlepotionverb"]+this.texto[language]["battleheal"].replace('VARHPINCREASE',increase);
        break;
      case "mpotion":
        this.hero.itens.mpotion -= 1;
        var increase = 49 + rollDice(6);
        this.hero.hp += increase;
        if (this.hero.hp > this.hero.maxhp) this.hero.hp = this.hero.maxhp;
        message = this.hero.name+this.texto[language]["battlempotionverb"]+this.texto[language]["battleheal"].replace('VARHPINCREASE',increase);
        break;
      case "remedy":
        this.hero.itens.remedy -= 1;
        this.hero.status = '';
        message += this.hero.name+this.texto[language]["battleremedyverb"]+this.texto[language]["battlecure"];
        break;
    }
    
    if (showmessage){
      this.messageWindow.showMensagem([message],function(context){/*does nothing*/});
    }else{
      return message;
    }
  },

  miracleEvent: function(prayer,showmessage){
    var message = this.hero.name + this.texto[language]["battleprayverb"];  
    var tpcost = prayer.cost;

    if (this.hero.tp >= tpcost){
      var diceresult = rollDice(prayer.dice);
      var pts = 0;
      switch(prayer.action){
        case "dmg": 
          message += this.texto[language]["battlemiracleonlybattle"];
          break;
        case "heal": 
          pts = prayer.pts + diceresult;
          message += this.texto[language]["battleheal"].replace('VARHPINCREASE',pts);
          this.hero.hp += pts;
          if (this.hero.hp > this.hero.maxhp) this.hero.hp = this.hero.maxhp;
          this.hero.tp -= tpcost;
          if (this.hero.tp <= 0) this.hero.tp = 0;
          break;
        case "cure": 
          this.hero.status = '';
          message += this.texto[language]["battlecure"];
          this.hero.tp -= tpcost;
          if (this.hero.tp <= 0) this.hero.tp = 0;
          break;
      }
    }else{
      message += this.texto[language]["battlemiracle0"];
    }

    if (showmessage){
      this.messageWindow.showMensagem([message],function(context){/*does nothing*/});
    }else{
      return message;
    }
  },

  setShopWindow: function(){
    if (this.paused){
      return false;
    }

    this.hideButtons();
    this.shopWindow.updatePage();
    this.shopWindow.visible = true;
  },

  innEvent: function(){
    if (this.paused){
      return false;
    }

    this.hideButtons();
    var cost = this.hero.level * 3;
    this.innWindow = new ChoiceWindow(this.game,this.texto[language]["innconfirmation"].replace("VARINNCOST",cost),this,
    this.texto[language]["yes"],this.texto[language]["no"],
      function(){
        if(sfxOn===true){
          this.selectSound.play();
        }        
        this.healPlayer(cost);
        this.innWindow.destroy();
        //this.overlay.alpha = 0;
      },
      function(){
        if(sfxOn===true){
          this.cancelSound.play();
        }
        this.innWindow.destroy();
        this.showButtons(false);
        //this.overlay.alpha = 0;
      }
    );
  },
  
  healPlayer: function(cost){
    if (typeof cost == 'undefined') cost = 0;
    if (cost <= this.hero.gold){
      this.messageWindow.showMensagem([
        this.texto[language]["innrest1"],
        this.texto[language]["innrest2"]
      ],
      function(context){
        context.showButtons(false);
      });
      this.hero.hp = this.hero.maxhp;
      this.hero.tp = this.hero.maxtp;
      if (cost > 0) this.hero.gold -= cost;
    }else{
      this.messageWindow.showMensagem([
        this.texto[language]["innoutofmoney"]
      ],
      function(context){
        context.showButtons(false);
      });
    }
    
  },

  setTavernScene: function(){
    if (this.paused){
      return false;
    }

    this.hideButtons();
    this.tavernsystem.showPeopleList();
    //this.tavernsystem.getConversation();
  },

  tellPlayerAboutLevelUp: function(atributo){
    /*var msgEnemy = this.texto[language]["levelupnormal"];
    if (this.level >= global_dragonLevel){
      msgEnemy = this.texto[language]["levelupboss"];
    }*/

    this.messageWindow.showMensagem([
      this.texto[language]["levelup"+atributo],
      this.texto[language]["leveluphp"],
      //msgEnemy,
      this.texto[language]["levelupcourage"],
    ],
    function(context){
      context.setExpWindow();
    });
  },

  resetHero: function(){
    this.hero.hp = this.hero.maxhp;
    this.hero.tp = this.hero.maxtp;
    this.hero.gold = 100;
    this.hero.attack = 0;
    this.hero.defense = 0;
    this.hero.speed = 0;
    this.hero.info = 0;
    this.hero.weapon_id = 0, 
    this.hero.shield_id = 0, 
    this.hero.tool_id = 0, 
    this.hero.book_id = 0, 
    this.hero.status = "";
    this.hero.itens = {};
    //this.hero.exp = 0;
    this.hero.floor = 1;
    this.hero.tentativas++;
    
    this.bossmode = false; 
    this.reward = "";
    this.wave = 0;
    this.maxwave = 0;
    this.saveGame();
  },
  
  /** 
   * 1 a 4: Ouro
   * 5: Poção
   * 6: Chave
   * 7: Bônus Arma
   * 8: Bônus Escudo
   * 9: Bônus Treino
   * 10: Bônus Livro
  */
  giveItemToPlayer: function(level,dice,msgOpen, camefromevent){
    if(typeof dice == 'undefined') 
      dice = rollDice(6);
    if(typeof msgOpen == 'undefined') 
      msgOpen = this.texto[language]["treasurechestopen"];
    var expReward = level * global_baseExp;
    var msgExp = this.texto[language]["treasurechestexp"].replace('VAREXPREWARD',expReward);
    
    switch(dice){
      case 0:
        this.messageWindow.showMensagem([
          msgOpen,
          this.texto[language]["eventwonexp"].replace('VARPTS',expReward)
        ],
        function(context){
          context.expwave += expReward;
          context.eventsystem.close();
        });
        break;
      case 1: case 2: case 3: case 4: //Ouro
        dice = rollDice(2,level) * 10;
        this.messageWindow.showMensagem([
          msgOpen,
          this.texto[language]["treasurechestgold"].replace('VARGOLDCOINS',dice),
          msgExp
        ],
        function(context){
          context.goldwave += dice;
          context.expwave += expReward;
          context.eventsystem.close();
        });
        break;
      case 5: //Poção
        this.messageWindow.showMensagem([
          msgOpen,
          this.texto[language]["treasurechestpotion"],
          msgExp
        ],
        function(context){
          if (typeof context.hero.itens.potion == 'undefined'){
              context.hero.itens.potion = 1;
          }else{
              context.hero.itens.potion += 1;
          }
          context.expwave += expReward;
          context.eventsystem.close();
        });
        break;
      case 6: //Chave
        this.messageWindow.showMensagem([
          msgOpen,
          this.texto[language]["treasurechestkey"],
          msgExp
        ],
        function(context){
          if (typeof context.hero.itens.key == 'undefined'){
              context.hero.itens.key = 1;
          }else{
              context.hero.itens.key += 1;
          }
          context.expwave += expReward;
          context.eventsystem.close();
        });
        break;
    }
  },

  debugLvUp: function(){
    if (this.paused){
      return false;
    }
    /*this.hero.exp = nextLevelDnD(this.hero.level,global_baseExp,global_expoent);
    this.hero.gold = 99999;
    this.setExpWindow();*/
    //this.finishGame();
    //this.angleBarkm2j.visible = false;
    //this.angleBar.visible = true;
    //this.angleBar.startCursor(this.hero.floor,this.hero.kno+this.hero.info);
  },
  
  hideStartMessage: function() {
//    this.startMessage.visible = false;
//    this.narratorMessage.visible = false;
//    this.winPoseSpr.visible = false;
//    this.messageBG.visible = false;
//    this.ball.visible = true;
//    this.playerSpr.input.enableDrag();
//    if(this.gamemode == 'B') this.matchTimer.start();
//    
//    // READ USER INPUT
//    this.game.input.onDown.add(this.handlePointerDown,this);
  },

  finishGame: function(){
    this.game.plugin.fadeAndPlay("rgb(0,0,0)",2,"Ending");
  },

  openOptions: function() {
    if (this.paused || this.messageWindow.visible == true){
      return false;
    }
    
    this.overlay.alpha = 0.5;
    this.paused = true;
    this.optWindow = new OptionWindow(this.game,this,false);
  },

  unpauseGame: function(){
    this.overlay.alpha = 0;
    this.paused = false;    
  },

  saveGame: function(){    
    playerData[this.saveslot] = this.hero;
    localStorage["com.hachicom.hachirpg.playerData"] = JSON.encode(playerData); 
  },
  
  endGame: function() {
    /*this.startMessage.setText(glossary.text.nolife[language]);
    this.narratorMessage.setText(glossary.text.gameover[language]);
    this.startMessage.visible = true;
    this.startMessage.alpha = 0;
    this.fadeTween.start();
    this.narratorMessage.visible = true;
    this.narratorMessage.x = this.game.width;
    this.moveTween.start();
    this.messageBG.visible = true;
    this.gameover = true;
    this.gameoverTimer.start();
    // if(isMobile()) isPlayingBGM = false;
    // currentBGM.stop();
    // if(sfxOn===true) this.overSound.play();*/
  },
  
  showResults: function() {
    /*var paramArr = [this.score,this.strikes,this.totalStrikes,this.spares,this.totalSpares,this.diamonds,this.gamemode]
    this.game.plugin.fadeAndPlay("rgb(0,0,0)",2,"Gameover",paramArr);*/
  },
  
  pauseGame: function() {
    //console.log("clicked pause button");
    /*this.startMessage.setText("PAUSED");
    this.startMessage.visible = true;
    this.startMessage.alpha = 1;
    this.messageBG.visible = true;
    this.quitButton.show(true);
    this.resuButton.show(true);
    if(sfxOn===true){
      //this.selectSound.play();
      //TODO: use lowlatency plugin here
    }
    this.game.paused = true;
    this.paused = true;
    this.input.onDown.add(this.unpauseGame, this);*/
  },
};