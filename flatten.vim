" This is a Vim script, it runs inside Vim
"
" Open this file in Vim and type:
"   :source %
" Then type:
"   :messages
" To read the output
"
" --- mini FAQ ---
"
" Q: Why Vim script?
" A: Because it has a list behaviour similar to python and because I do not
" need to exit the editor to test the code.
"
" Q: Which version of Vim I need to run this?
" A: Vim 7.0 or any later version, must have more features than -tiny (-small,
" -big or -huge).


" This only flatten lists, dictionaries in lists with more lists inside will
" not be flattened.  If you have a list with dictionaries with lists you should
" probably define your own operations on that structure.
"
" Also, Vim has an (arbitrary) limit of 100 recursive calls.  This will not
" work for lists deeper than 100 sublists.
function! DeepFlattenList(input, result)
  for l:elem in a:input
    if type(l:elem) ==# type([])
      call DeepFlattenList(l:elem, a:result)
    else
      call add(a:result, l:elem)
    endif
  endfor
  return a:result
endfunction

" Wrapper, so we do not need to add the empty list every time
function! DeepFlatten(input)
  return DeepFlattenList(a:input, [])
endfunction

" Trivial testing procedure
function! Test(left, right)
  let l:out = v:null
  try
    execute 'let l:out = ' . a:right
  catch
  finally
    if type(a:left) ==# type(l:out) && a:left ==# l:out
      echom 'Test succeded'
    else
      echom 'Test failed, ' . string(a:left) ' != ' . string(l:out)
    endif
  endtry
endfunction

echom '--- Tests starting ---'

" good calls
call Test([], 'DeepFlatten([])')
call Test([{}], 'DeepFlatten([{}])')
call Test([1,2,3], 'DeepFlatten([[[1]],2, [3]])')
call Test(['a','b','c'], 'DeepFlatten(["a","b","c"])')
call Test([1,2,'yay'], 'DeepFlatten([[[1]],2, ["yay"]])')
call Test([1,{'nope':[1]},3], 'DeepFlatten([[[1]],{"nope":[1]}, [3]])')

" bad calls (exceptions)
call Test(v:null, 'DeepFlatten()')
call Test(v:null, 'DeepFlatten(1)')
call Test(v:null, 'DeepFlatten({})')
call Test(v:null, 'DeepFlatten({"nope":[1]})')
call Test(v:null, 'DeepFla([[[1]],{"nope":[1]}, [3]])')

