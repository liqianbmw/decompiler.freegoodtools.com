   "use strict"
   var isPolyfill=false;
   $(document).ready( function() {
      $("#del").on("change", function() { OnDelChange() });
      $("#charsel").on("change", function() {
         OnEncodingChange();
         var iencode = document.getElementById("charsel").selectedIndex;
         if( isPolyfill==false && iencode>2 )
            loadEncodingScripts();
      });
      if( typeof TextEncoder !== "function" ) {
         loadEncodingScripts();
      }
      $("#txt").on("dragover", function(event) {
         event.preventDefault();
         event.stopPropagation();
         $(this).addClass('draghover');
         return false;
      });
      $("#txt").on("dragleave dragend", function(event) {
         event.preventDefault();
         event.stopPropagation();
         $(this).removeClass('draghover');
         return false;
      });
      $("#txt").on("drop", function(event) {
         event.preventDefault();
         //event.stopPropagation();
         $(this).removeClass('draghover');
         var file = event.originalEvent.dataTransfer.files[0]
         fileLoad(file);
      });
      //var txt="$鈧悙佛き�";
      //var txt="$垄啶光偓饜崍";
      //$("#txt").val(txt);
   });
   function loadEncodingScripts()
   {
      isPolyfill=true;
      window.TextEncoder = window.TextDecoder = null;
      var s1 = document.createElement('script');
      s1.onload=function() {
         var s2 = document.createElement('script');
         //s2.onload=function() {
         //};
         //s2.type = "text/javascript";
         //s2.async = true;
         s2.src = "/lib/text-encoding/encoding.js";
         //s2.setAttribute('src', '/lib/text-encoding/encoding.js');
         document.body.appendChild(s2);
      };
      s1.src = "/lib/text-encoding/encoding-indexes.js";
      document.body.appendChild(s1);
   }
   function OnReset()
   {
      document.getElementById("deltxt").disabled=true;
   }
   function OnViewSelection()
   {
      var iencode = document.getElementById("charsel").selectedIndex;
      if( iencode>1 ) return;
      var start=document.getElementById("txt").selectionStart;
      var end=document.getElementById("txt").selectionEnd;
      //console.log(start+" "+end);
      if( end-start==0 ) return;
      OnConvert();
      var del = document.calcform.del.value;
      var idel = document.calcform.del.selectedIndex;
      var dellen=1;
      if( idel=2 ) dellen=0;
      if( idel=3 ) dellen=del.length;
      var len=8+dellen;
      /*
      if( iencode==2 )
      {
         for(var i=0; i<
      }
      */
      document.getElementById("bin").focus();
      document.getElementById("bin").selectionStart = len*start;
      document.getElementById("bin").selectionEnd = len*end-dellen;
   }
   function OnEncodingChange()
   {
      var iencode = document.getElementById("charsel").selectedIndex;
      if( iencode<2 )
         document.getElementById("viewsel").disabled = false;
      else
         document.getElementById("viewsel").disabled = true;
   }
   function OnDelChange()
   {
      var idel = document.calcform.del.selectedIndex;
      if( idel==3 )
      {
         document.getElementById("deltxt").disabled=false;
      }
      else
      {
         document.getElementById("deltxt").disabled=true;
         document.getElementById("deltxt").value="";
      }
   }
   function OnOpen()
   {
      // $("#fileElem").click();
      $("#file").click();
   }
   function OnFile()
   {
      var file = document.getElementById("fileElem").files[0];
      document.getElementById("fileElem").value="";
      // fileLoad(file);
   }
   function OnSave()
   {
      //var file=$("#file").val();
      //if( file=="" ) file="file.txt";
      fileSave("binary-output.txt");
   }
   function OnBinSave()
   {
      fileBinSave("binary-output.bin");
   }
   function fileLoad(file)
   {
      var reader = new FileReader();
      reader.onloadend=function(e) {
         if( e.target.readyState==FileReader.DONE ) {
            var txt = e.target.result;
            $("#txt").val(txt);
            $("#txt").focus();
         }
      };
      reader.readAsText(file, "UTF-8");
   }
   function fileSave(filename)
   {
      var txt=$("#bin").val();
      if( txt=="" ) return;
      var blob = new Blob([txt], {type: "text/plain;charset=utf-8"});
      saveAs(blob, filename);
   }
   function fileBinSave(filename)
   {
      var txt=$("#bin").val();
      if( txt=="" ) return;
      var del = document.calcform.del.value;
      var idel = document.calcform.del.selectedIndex;
      if( idel==0 ) del=" ";
      else if( idel==1 ) del=",";
      else if( idel==3 )
         del=document.getElementById("deltxt").value;
      var arr=txt.split(del);
      var bytes=[];
      for(var i=0; i<arr.length; i++)
         bytes[i]=parseInt(arr[i],2);
      var b=new Uint8Array(bytes);
      var blob = new Blob([b], {type: "application/octet-stream"});
      saveAs(blob, filename);
   }
   function OnConvert()
   {
      var txt = document.calcform.txt.value;
      var iencode = document.getElementById("charsel").selectedIndex;
      var del = document.calcform.del.value;
      var idel = document.calcform.del.selectedIndex;
      if( idel==0 ) del=" ";
      else if( idel==1 ) del=",";
      else if( idel==3 )
         del=document.getElementById("deltxt").value;
      //var len = [...txt].length;  // "馃攽".length=2
      var bin='';
      if( iencode<2 )
      {
         if( txt.length==0 ) return;
         for(var i=0; i<txt.length; i++)
         {
            var a = txt.codePointAt(i);
            /*
            var a;
            if( iencode==0 )
               a = txt.charCodeAt(i);
            else
               a = txt.codePointAt(i);
            */
            var b = a.toString(2);
            if( b.length<8 ) b='0'.repeat(8-b.length)+b;
            bin += b;
            bin+=del;
            if( b.length>16 ) i++;
         }
      }
      else
      {
         var encoding = document.getElementById("charsel").value;
         var bytes;
         if( isPolyfill==false )
            bytes = new TextEncoder(encoding).encode(txt);
         else
            bytes = new TextEncoder(encoding, { NONSTANDARD_allowLegacyEncoding: true }).encode(txt);
         //bytes = bytes.split(",");
         for(var i=0; i<bytes.length; i++)
         {
            var b=bytes[i].toString(2);
            if( b.length<8 ) b='0'.repeat(8-b.length)+b;
            bin+=b;
            bin+=del;
         }
      }
      if( bin[bin.length-1]==del ) bin=bin.substring(0,bin.length-1);
      document.getElementById("bin").value = bin;
   }
   function OnSelect()
   {
      document.calcform.bin.select();
   }
   function OnCopy()
   {
      $("#bin").select();
      document.execCommand("copy");
   }