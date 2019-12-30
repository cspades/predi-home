function time = time_samp(t,T)
    c = (t-1) * T;
    [s, m, h] = ct(c);
    time = [s, m, h];
end

function [s, m, h] = ct(sec)
    s = rem(sec,60);
    m = floor(rem(sec,3600)/60);
    h = floor(sec/3600);
end