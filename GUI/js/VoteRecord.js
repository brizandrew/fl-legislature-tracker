function VoteRecord(config){
	this.vote = config.vote;
	this.name = config.name;
	this.number = config.number;
	this.summary = config.summary;
	this.fullTextURL = config.fullTextURL;
	this.url = config.url;

	this.ele;
	this._init();
	return this.ele;
};

VoteRecord.prototype._init = function() {
	this.ele = document.createElement("ul");

	var nameLi = document.createElement("li");
	var nameHead = document.createElement("h5");
	var nameA = document.createElement("a");
	nameA.href = this.url;
	nameA.innerHTML = this.number + ": " + this.name;

	var voteLi = document.createElement("li");
	voteLi.className = "vote";

	var summaryLi = document.createElement("li");
	summaryLi.innerHTML = this.summary;

	var fullTextLi = document.createElement("li");
	fullTextLi.className = "fullTextLink";
	var fullTextA = document.createElement("a");
	fullTextA.href = this.fullTextURL;
	fullTextA.innerHTML = "Full Text";

	if(this.vote == "Y"){
		this.ele.className = "result yea";
		voteLi.innerHTML = "Y";
	}
	else if(this.vote == "N"){
		this.ele.className = "result nay";
		voteLi.innerHTML = "N";
	}
	else if(this.vote == "-"){
		this.ele.className = "result abstain";
		voteLi.innerHTML = "A";
	}
	else{
		this.ele.className = "result noVote";
	}

	this.ele.appendChild(nameLi);
		nameLi.appendChild(nameHead);
			nameHead.appendChild(nameA);
	this.ele.appendChild(voteLi);
	this.ele.appendChild(summaryLi);
	this.ele.appendChild(fullTextLi);
		fullTextLi.appendChild(fullTextA);
}