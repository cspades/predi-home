function t = time_conv(s,m,h,T)
    t = floor(cs(s,m,h)/T) + 1;
end

function s = cs(s,m,h)
    s = h * 3600 + m * 60 + s;
end