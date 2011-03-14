var boggle;
var flash;
var query_state;
(function() {

/* The game of Boggle
 * Contains the game logic and components including the board,
 * add word widget, and word list.
 */
var Boggle = Class.create({
    initialize: function(node) {
        this._node = node;
        this._wordInput = new WordInput(this, this._node.down('#word'));
        this._wordList = new WordList(this, this._node.down('#word-list'));
        this._board = new Board(this, this._node.down('#board'));
        this._solutionSetHistory = [new SolutionSet()];
        this._timeLeft = new TimeLeft(this, this._node.down('#time-left'));
        $('time-left').observe('timeleft:done', this.endRound.bindAsEventListener(this));
        $('word-list').observe('wordlist:compared', this.submitScore.bindAsEventListener(this));
        this._active = true;
    },
    /********************************************************/
    /* QUERIES                                              */
    /********************************************************/
    solutionSetDeltaForLetter: function(letter) {
        // If any solutions are possible by applying letter to
        // any of the existing solutions, return the solution
        // set delta.
        var solutionSet = this._solutionSetHistory.last();
        var candidates = this._board.cellsForLetter(letter);
        if (!candidates) return false; // This letter is not on the board
        
        // If this is the first letter, no need to check further.
        if (solutionSet.empty()) return new SolutionSetDelta(candidates);

        var delta = new SolutionSetDelta();
        solutionSet.each(function(delta, candidates, solution, index) {
            for (var i=0; i<candidates.length; i++) {
                var cell = candidates[i];
                var badCandidate = false;
                // Is cell already in the solution?
                badCandidate |= solution.has(cell);
                // Is cell adjacent to the last cell in the solution?
                badCandidate |= !this._board.adjacent(cell, solution.lastCell());
                if (!badCandidate) {
                    delta.addCellForSetIndex(cell, index);
                }
            }
        }.bind(this, delta, candidates));
        return delta.empty() ? false : delta;
    },
    solutionSetDeltaForCell: function(cell) {
        // If any solutions are possible by applying letter to
        // any of the existing solutions, return the solution
        // set delta.
        var solutionSet = this._solutionSetHistory.last();
        
        // If this is the first letter, no need to check further.
        if (solutionSet.empty()) return new SolutionSetDelta($A([cell]));

        var delta = new SolutionSetDelta();
        solutionSet.each(function(delta, cell, solution, index) {
            var badCandidate = false;
            // Is cell already in the solution?
            badCandidate |= solution.has(cell);
            // Is cell adjacent to the last cell in the solution?
            badCandidate |= !this._board.adjacent(cell, solution.lastCell());
            if (!badCandidate) {
                delta.addCellForSetIndex(cell, index);
            }
        }.bind(this, delta, cell));
        return delta.empty() ? false : delta;
    },
    /********************************************************/
    /* COMMANDS    (MAKE CHANGE HERE [LIAM])                */
    /********************************************************/
    submitWord: function(word) {
        var form = $('word-form');
        var self = this;
        var numr = $("numrounds").readAttribute("rounds");
        new Ajax.Request(form.getAttribute('action'), {
            method: 'post',
            evalJS: true,
            postBody: 'word=' + word,
            onSuccess: function(transport){
              self.addWordToList(word,transport);
              var response = {"data":numr+','+word+','+ transport.responseJSON["score"],
                              "timestamp": (new Date).getTime()/1000.0};
             //console.log(response[]);
            new Ajax.Request('/study/send-data',{
                method: 'post',
                postBody:  
                  'data=' + response['data'] +
                  '&timestamp=' + response['timestamp'] +
                  '&code=BOG'
              });
            }
          /*this.addWordToList.curry(word).bindAsEventListener(this)*/
        });

    },
    addWordToList: function(word, response) {
        this._wordList.addWord(word, response.responseJSON);
    },
    applySolutionSetDelta: function(delta) {
        // Apply the delta to produce a new solution set.
        // Add the new solution set to the history of solution sets.
        var newSolutionSet = this._solutionSetHistory.last().solutionSetByApplyingDelta(delta);
        this._board.deactivateAllCells();
        this._board.applyActivationMap(newSolutionSet.getActivationMap());
        this._solutionSetHistory.push(newSolutionSet);
    },
    clearSolutionSetHistory: function() {
        // Remove all solution sets from the history and
        // clear the board activation.
        this._solutionSetHistory = [new SolutionSet()];
        this._board.deactivateAllCells();
    },
    undoLastSolutionSetDelta: function() {
        // Remove the most recent solution set from the history
        // and set the board activation to the previous set.
        this._solutionSetHistory.pop();
        this._board.deactivateAllCells();
        this._board.applyActivationMap(this._solutionSetHistory.last().getActivationMap());
    },
    endRound: function() {
        this._active = false;
        this._wordInput.turnOff();
        this._node.addClassName('inactive');
        $('next-round').show();
        new Ajax.Request($('compare-words').getAttribute('action'), {
            method: 'get',
            evalJS: true,
            onSuccess: this._wordList.compareWords.bind(this._wordList)
        });
    },
    submitScore: function() {
        var score = this._wordList.getScore()
        new Ajax.Request($('submit-score').getAttribute('action'), {
            method: 'post',
            postBody: 'score=' + score,
            onSuccess: this.updateScore.bind(this)
        })
    },
    updateScore: function() {
	//console.log(this);
    },
    /********************************************************/
    /* EVENT HANDLERS                                       */
    /********************************************************/
    onCellClick: function(cell, clicked) {
        var delta = this.solutionSetDeltaForCell(cell);
        if (delta) {
            this.applySolutionSetDelta(delta);
            this._wordInput.push(cell.letter);
        }
    }
});


var SolutionSet = Class.create({
    // A set of possible solutions for a given sequence of letters.
    initialize: function() {
        // An empty solution set.
        this._solutions = $A();
    },
    /********************************************************/
    /* QUERIES                                              */
    /********************************************************/
    solutionSetByApplyingDelta: function(delta) {
        // A new solution set by applying the delta
        newSolutionSet = new SolutionSet();
        if (this.empty()) {
            // delta will have a list of candidates
            newSolutionSet._solutions = delta.firstLetterCells().collect(function(cell) {
                return new Solution([cell]);
            });
        } else {
            delta._delta.each(function(newSolutions, pair) {
                var index = pair.key;
                var cells = pair.value;
                var oldSolution = this._solutions[index];
                for (var i=0; i<cells.length; i++) {
                    var cell = cells[i];
                    var newSolution = oldSolution.solutionByAppendingCell(cell);
                    newSolutions.push(newSolution);
                }
            }.bind(this, newSolutionSet._solutions));
        }
        return newSolutionSet;
    },
    getActivationMap: function() {
        if (!this._activationMap) {
            // An activation map indicates the special states of cells.
            // It is a mapping from states to lists of cells.
            this._activationMap = $H();
            if (this.empty()) return this._activationMap;
            this._activationMap.set('activate', $A());
            this._activationMap.set('markAsCandidate', $A());
            for (var i=0; i<this._solutions.first().getLength(); i++) {
                var cells = this._solutions.collect(function(i, sol) {return sol.cellAt(i)}.curry(i));
                if (cells.uniq().length > 1) {
                    cells.each(function (cell) {
                        this._activationMap.get('markAsCandidate').push(cell);
                    }.bind(this));
                } else {
                    this._activationMap.get('activate').push(cells.first());
                }
            }
        }
        return this._activationMap;
    },
    empty: function() {
        return this._solutions.length == 0;
    },
    toString: function() {
        return this._solutions.collect(function(sol, index) {
            return index + ': ' + sol.toString();
        }).join('\n');
    },
    each: function(iterator) {
        this._solutions.each(iterator);
    }
});


var Solution = Class.create({
    // A single path through the board which spells a given word.
    initialize: function(path) {
        this._path = $A(path); // copy
    },
    /********************************************************/
    /* QUERIES                                              */
    /********************************************************/
    solutionByAppendingCell: function(cell) {
        var newSolution = new Solution(this._path);
        newSolution._path.push(cell);
        return newSolution;
    },
    getLength: function() {
        return this._path.length;
    },
    cellAt: function(index) {
        return this._path[index];
    },
    lastCell: function() {
        return this._path.last();
    },
    has: function(cell) {
        return this._path.any(function (cell1, cell2) {
            return cell1 == cell2;
        }.curry(cell));
    },
    toString: function() {
        return '['+this._path.collect(function(cell) {return cell.getId()}).join(',')+']';
    }
});


var SolutionSetDelta = Class.create({
    initialize: function(firstLetterCells) {
        // mapping of setIndices to lists of cells
        this._delta = $H();
        if (firstLetterCells) {
            // This is a delta to be applied to an empty
            // solution set.
            this._delta.set('firstLetterCells', firstLetterCells);
        }
    },
    /********************************************************/
    /* QUERIES                                              */
    /********************************************************/
    cellsForSetIndex: function(index) {
        return this._delta.get(index);
    },
    empty: function() {
        return this._delta.keys().length == 0;
    },
    firstLetterCells: function() {
        return this._delta.get('firstLetterCells');
    },
    /********************************************************/
    /* COMMANDS                                             */
    /********************************************************/
    addCellForSetIndex: function(cell, index) {
        var cells = this._delta.get(index) || $A();
        cells.push(cell);
        this._delta.set(index, cells);
    }
});


var Board = Class.create({
    initialize: function(game, node) {
        this._node = $(node);
        this._makeDOM();
        this._game = game;
        this._cells = this._node.select('.cell').collect(function(node) {return new Cell(this._game, node)}.bind(this));
        // Mapping from cell nodes to Cell objects.
        this._idToCell = $H();
        this._cells.each(function(cell) {this._idToCell.set(cell._node.id, cell)}.bind(this));
        // Mapping from letters to lists of cells.
        this._letterToCells = $H();
        this._cells.each(function(cell) {
            var cells = this._letterToCells.get(cell.letter) || $A();
            cells.push(cell);
            this._letterToCells.set(cell.letter, cells);
            }.bind(this));
    },
    _makeDOM: function() {
        var cellValues = this._node.getAttribute('cells').split(' ');
        var shape = this._node.getAttribute('shape').split(' ');
        var width = new Number(shape[0]);
        var height = new Number(shape[1]);
        this._node.insert({top: '<div class="container"></div>'});
        var container = this._node.down('.container');
        container.insert({top: '<div id="board-blocker"><h1>Round finished!</h1><h1>Click on <span style="padding: 3px; background-color:#369; color:white">Next Round</span> <br/>to continue</h1></div>'});
        var row, col;
        for (var rowIndex=0; rowIndex<height; rowIndex++) {
            row = new Element('div', {
                'class': 'row row' + rowIndex
                });
            container.insert({bottom: row});
            for (var colIndex=0; colIndex<width; colIndex++) {
                var letter = cellValues[rowIndex * width + colIndex];
                col = new Element('div', {
                    id: 'cell-' + rowIndex + '-' + colIndex,
                    'class': 'cell col' + colIndex,
                    letter: letter
                    });
                col.innerHTML = letter.replace(/^\*/, '');
                row.insert({bottom: col});
            }
        }
    },
    /********************************************************/
    /* QUERIES                                              */
    /********************************************************/
    adjacent: function(cell1, cell2) {
        // Are cell1 and cell2 adjacent?
        var a = cell1.position();
        var b = cell2.position();
        var adjacent = true;
        return (cell1.getId() !== cell2
            && (a[0] - b[0]).abs() <= 1
            && (a[1] - b[1]).abs() <= 1
        )
    },
    cellsForLetter: function(letter) {
        return this._letterToCells.get(letter);
    },
    /********************************************************/
    /* COMMANDS                                             */
    /********************************************************/
    deactivateAllCells: function() {
        this._cells.invoke('deactivate');
    },
    applyActivationMap: function(activationMap) {
        // Keys are function names, values are cells
        // For example:
        // {
        //    activate: [cell, cell, cell, ...],
        //    markAsCandidate: [cell, cell, cell, ...]
        // }
        activationMap.each(function(item) {
            // For example:
            // [cell, cell, cell].invoke('activate');
            item.value.invoke(item.key);
        });
    }
});


var Cell = Class.create({
    initialize: function(game, node) {
        this._node = $(node);
        this._game = game;
        this._note = node.down('.note');
        // Attributes
        this.letter = this._node.getAttribute('letter');
        this._special = this.letter.startsWith('*');
        this.letter = this.letter.replace(/Qu/, 'Q').replace(/^\*/, '');
        if (this._special) {
            this._node.addClassName('special');
        }
        // Event handlers
        this._node.observe('click', this._game.onCellClick.curry(this).bindAsEventListener(this._game));
    },
    /********************************************************/
    /* QUERIES                                              */
    /********************************************************/
    getId: function() {
        return this._node.id;
    },
    position: function() {
        // [col, row]
        var match = this._node.id.match(/^cell-(\d+)-(\d+)$/);
        return [new Number(match[2]), new Number(match[1])];
    },
    /********************************************************/
    /* COMMANDS                                             */
    /********************************************************/
    activate: function() {
        this._node.addClassName('active');
    },
    markAsCandidate: function() {
        this._node.addClassName('candidate');
    },
    deactivate: function() {
        this._node.removeClassName('active');
        this._node.removeClassName('candidate');
    }
});


var WordInput = Class.create({
    initialize: function(game, node) {
        this._node = node;
        this._game = game;  
        // Used to map keyCode to letters starting at 65
        this._codeForA = 65;
        this._codeMap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        // Clear value on page refresh.
        this._node.setValue('');
        // Register event handler        
        this.turnOn();
    },
    /********************************************************/
    /* QUERIES                                              */
    /********************************************************/
    getLength: function() {
        return this._node.getValue().length;
    },
    getValue: function() {
        return this._node.getValue();
    },
    /********************************************************/
    /* COMMANDS                                             */
    /********************************************************/
    push: function(letter) {
        // Append a letter to the end of input
        this._node.setValue(this._node.getValue() + letter);
    },
    pop: function() {
        // Remove and return last letter in input
        var v = this._node.getValue();
        var i = 1 + v.endsWith('Qu');
        this._node.setValue(v.slice(0, v.length - i));
        return v[v.length - i];
    },
    reset: function() {
        // Remove all letters from input
        this._node.setValue('');
    },
    turnOn: function() {
        document.observe('keydown', this.onKey.bindAsEventListener(this));
    },
    turnOff: function() {
        document.stopObserving('keydown');
    },
    /********************************************************/
    /* EVENT HANDLERS                                       */
    /********************************************************/
    onKey: function(event) {
        if (event.keyCode == Event.KEY_ESC) {
            event.stop();
            this._game.clearSolutionSetHistory();
            this.reset();
        }
        if (event.keyCode == Event.KEY_BACKSPACE) {
            event.stop();
            if (this.getLength() > 0) {
                this._game.undoLastSolutionSetDelta();
                this.pop();
            }
        }
        if (event.keyCode == Event.KEY_RETURN) {
            event.stop();
            if (this.getLength() > 2) {
                this._game.submitWord(this.getValue());
                this._game.clearSolutionSetHistory();
                this.reset();
            } else {
                flash.show('Word must be at least 3 letters long.');
            }
        }
        if (event.keyCode >= 65 && event.keyCode <= 90) {
            event.stop();
            // Letters A through Z
            var letter = this._codeMap[event.keyCode - this._codeForA];
            var delta = this._game.solutionSetDeltaForLetter(letter);
            if (delta) {
                this._game.applySolutionSetDelta(delta);
                this.push(letter.replace('Q', 'Qu'));
            }
        }
    }
});


var WordList = Class.create({
    initialize: function(game, node) {
        this._node = node;
        this._game = game;
        this._score = node.down('#score');
    },
    /********************************************************/
    /* QUERIES                                              */
    /********************************************************/
    getScore: function() {
        return new Number(this._score.down('.score').innerHTML);
    },
    /********************************************************/
    /* COMMANDS                                             */
    /********************************************************/
    addWord: function(word, wordAttributes, bottom) {
        var wordNode = new Element('div');
        wordNode.setAttribute('word', word);
        wordNode.setAttribute('score', wordAttributes['score']);
        wordNode.innerHTML = word + '<span class="score">' + wordAttributes['score'] + '</span>';
        wordNode.addClassName('word');
        wordNode.addClassName(wordAttributes['valid'] ? 'valid' : 'invalid');
        if (wordAttributes['duplicate']) wordNode.addClassName('duplicate');
        if (wordAttributes['other']) wordNode.addClassName('other');
        if (bottom) {
            this._node.insert({bottom: wordNode});
        } else {
            this._score.insert({after: wordNode});            
        }
        var score = new Number(this._score.down('.score').innerHTML);
        this._score.down('.score').innerHTML = score + wordAttributes['score'];
    },
    adjustScoreBy: function(value) {
        var score = new Number(this._score.down('.score').innerHTML);
        this._score.down('.score').innerHTML = score + value;
    },
    reset: function() {
        this._node.innerHTML = '<div id="score" class="word">score<span class="score">' + this._score.down('.score').innerHTML + '</span></div>';
    },
    compareWords: function(transport) {
        my = transport.responseJSON.my;
        common = transport.responseJSON.common;
        other = transport.responseJSON.other;
        this._node.select('.word.valid').each(function(word_node) {
            var word = word_node.getAttribute('word');
            var score = word_node.getAttribute('score');
            if (common.member(word)) {
                word_node.addClassName('common');
                word_node.setAttribute('score', 0);
                word_node.down('.score').innerHTML = 0;
                this.adjustScoreBy(-score);
            }
        }.bind(this));
        other.each(function(word) {
            this.addWord(word, {valid: true, duplicate: false, other: true, score: 0}, true);
        }.bind(this));
        this._node.fire('wordlist:compared');
    }
});


var TimeLeft = Class.create({
    initialize: function(game, node) {
        this._node = $(node);
        this._game = game;
        this._timer = null;
        this._value = null;
        new Ajax.Request(this._node.getAttribute('updateURL'), {
            evalJSON: true,
            onSuccess: this.setInitialValue.bind(this)
        });
    },
    setInitialValue: function(transport) {
        this._value = transport.responseJSON;
        this._node.innerHTML = (Math.floor(this._value/60)) +":"+(String("0" + this._value%60).slice(-2));
        this._timer = setTimeout(this.decrementValue.bind(this), 1000);
    },
    decrementValue: function() {
        this._value--;
        if (this._value >= 0) {
            this._node.innerHTML = (Math.floor(this._value/60)) +":"+(String("0" + this._value%60).slice(-2));
            this._timer = setTimeout(this.decrementValue.bind(this), 1000);
        } else {
            this._node.fire('timeleft:done');
        }
    }
});


var Flash = Class.create({
    initialize: function(node) {
        this._node = $(node);
        this._timer = null;
    },
    /********************************************************/
    /* COMMANDS                                             */
    /********************************************************/
    show: function(message) {
        this._node.innerHTML = message;
        if (this._timer) {
            clearTimeout(this._timer);
            this._timer = null;
        }
        this._node.show();
        this._timer = setTimeout(this.hide.bindAsEventListener(this), 1500);
    },
    hide: function() {        
        this._node.fade();
        this._timer = null;
    }
});


var QueryState = Class.create({
    initialize: function(node) {
        this._node = node;
        this._url = node.getAttribute('action');
        this._currentState = new Number(node.getAttribute('currentState'));
        this._currentRound = new Number(node.getAttribute('roundId'));
	//console.log(this._currentState, this._currentRound);
        this._waiting = false;
        // this._timer = setTimeout(this.sendQuery.bindAsEventListener(this), 1000);
    },
    sendQuery: function() {
        if (!this._waiting) {
            new Ajax.Request(this._url, {
                method: 'get',
                evalJS: true,
                onSuccess: this.handleStateResponse.bindAsEventListener(this)
            });
            this._waiting = true;
        }
        this._timer = setTimeout(this.sendQuery.bindAsEventListener(this), 1000);        
    },
    handleStateResponse: function(transport) {
        var info = transport.responseJSON;
	//console.log(info.state, info.round);
        
        if (info.state!=this._currentState || info.round != this._currentRound) {
            window.location = window.location;
        }
        this._waiting = false;
    }
});


document.observe('dom:loaded', function(loaded) {
    var boggle_node = $('game');
    query_state = new QueryState($('query-state'));        
    if(boggle_node.down('#board')) {
        boggle = new Boggle(boggle_node);
        flash = new Flash($('flash-message'));        
    }
});
})()
